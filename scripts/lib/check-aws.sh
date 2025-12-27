#!/bin/bash
# Shared utility to check AWS CLI installation and credentials

# Detects all available AWS profiles from config and credentials files
# Returns: Space-separated list of profile names
detect_aws_profiles() {
  local profiles=()

  # Parse ~/.aws/config for [profile xyz] or [default]
  if [ -f ~/.aws/config ]; then
    while IFS= read -r line; do
      if [[ "$line" =~ ^\[profile\ (.+)\] ]]; then
        profiles+=("${BASH_REMATCH[1]}")
      elif [[ "$line" =~ ^\[default\] ]]; then
        profiles+=("default")
      fi
    done < ~/.aws/config
  fi

  # Parse ~/.aws/credentials for [xyz]
  if [ -f ~/.aws/credentials ]; then
    while IFS= read -r line; do
      if [[ "$line" =~ ^\[(.+)\] ]]; then
        local prof="${BASH_REMATCH[1]}"
        # Add if not already in list
        if [[ ! " ${profiles[@]} " =~ " ${prof} " ]]; then
          profiles+=("$prof")
        fi
      fi
    done < ~/.aws/credentials
  fi

  echo "${profiles[@]}"
}

# Get profile info for display
# Args: $1 - profile name
# Returns: Info string (type and region)
get_profile_info() {
  local profile="$1"
  local info=""
  local region=""

  # Check if SSO
  if is_sso_profile "$profile"; then
    info="SSO"
  else
    info="Standard"
  fi

  # Get region from config
  if [ -f ~/.aws/config ]; then
    local in_profile=false
    while IFS= read -r line; do
      if [[ "$line" =~ ^\[profile\ ${profile}\] ]] || [[ "$line" =~ ^\[${profile}\] ]]; then
        in_profile=true
      elif [[ "$line" =~ ^\[.*\] ]]; then
        in_profile=false
      elif [ "$in_profile" = true ]; then
        if [[ "$line" =~ ^region\ *=\ *(.+)$ ]]; then
          region="${BASH_REMATCH[1]}"
          region=$(echo "$region" | xargs) # trim whitespace
          break
        fi
      fi
    done < ~/.aws/config
  fi

  if [ -n "$region" ]; then
    info="$info, $region"
  fi

  echo "$info"
}

# Prompts user to select a profile from list
# Args: $@ - list of profile names
# Returns: Selected profile name via echo
select_aws_profile() {
  local profiles=("$@")

  echo "Multiple AWS profiles detected:" >&2
  echo "" >&2

  local i=1
  for profile in "${profiles[@]}"; do
    local profile_info=$(get_profile_info "$profile")
    printf "  %d) %-40s (%s)\n" "$i" "$profile" "$profile_info" >&2
    i=$((i + 1))
  done

  echo "" >&2
  read -p "Select profile (1-${#profiles[@]}): " selection

  # Validate selection
  if [[ "$selection" =~ ^[0-9]+$ ]] && [ "$selection" -ge 1 ] && [ "$selection" -le "${#profiles[@]}" ]; then
    echo "${profiles[$((selection - 1))]}"
  else
    echo "Error: Invalid selection" >&2
    exit 1
  fi
}

# Check if profile uses SSO
# Args: $1 - profile name
# Returns: 0 if SSO, 1 if not
is_sso_profile() {
  local profile="$1"

  if [ -f ~/.aws/config ]; then
    # Look for sso_session or sso_start_url in profile section
    local in_profile=false
    while IFS= read -r line; do
      if [[ "$line" =~ ^\[profile\ ${profile}\] ]] || [[ "$line" =~ ^\[${profile}\] ]]; then
        in_profile=true
      elif [[ "$line" =~ ^\[.*\] ]]; then
        in_profile=false
      elif [ "$in_profile" = true ]; then
        if [[ "$line" =~ ^sso_session ]] || [[ "$line" =~ ^sso_start_url ]]; then
          return 0
        fi
      fi
    done < ~/.aws/config
  fi

  return 1
}

# Check if OIDC credentials are already configured
# Returns: 0 if OIDC authenticated, 1 if not
is_oidc_authenticated() {
  # Try to call STS without profile to see if credentials work
  if aws sts get-caller-identity > /dev/null 2>&1; then
    return 0
  fi
  return 1
}

check_aws_configured() {
  local aws_cmd="aws"
  local profile_flag=""

  # Check if AWS CLI is installed
  if ! command -v aws > /dev/null 2>&1; then
    echo "Error: AWS CLI is not installed."
    echo ""
    echo "Please install the AWS CLI to use this script:"
    echo ""
    echo "macOS (Homebrew):"
    echo "  brew install awscli"
    echo ""
    echo "macOS/Linux (official installer):"
    echo "  curl \"https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip\" -o \"awscliv2.zip\""
    echo "  unzip awscliv2.zip"
    echo "  sudo ./aws/install"
    echo ""
    echo "Or visit: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
  fi

  # Check if OIDC credentials are already configured (e.g., in GitHub Actions)
  if is_oidc_authenticated; then
    echo "Using existing AWS credentials (OIDC or environment variables)"
    echo ""

    # Verify and display caller identity
    CALLER_IDENTITY=$(aws sts get-caller-identity 2>&1)
    RESULT_CODE=$?

    if [ $RESULT_CODE -eq 0 ]; then
      echo "AWS credentials verified!"

      # Parse and display key info
      if command -v jq > /dev/null 2>&1; then
        ACCOUNT=$(echo "$CALLER_IDENTITY" | jq -r '.Account')
        ARN=$(echo "$CALLER_IDENTITY" | jq -r '.Arn')
        echo "  Account: $ACCOUNT"
        echo "  Identity: $ARN"
      else
        # Fallback without jq
        ACCOUNT=$(echo "$CALLER_IDENTITY" | grep -o '"Account"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"Account"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
        if [ -n "$ACCOUNT" ]; then
          echo "  Account: $ACCOUNT"
        fi
      fi

      echo ""

      # Export empty profile to signal OIDC authentication to caller
      export AWS_PROFILE=""
      return 0
    fi
  fi

  # Auto-detect profile if not set
  if [ -z "$AWS_PROFILE" ]; then
    local available_profiles=($(detect_aws_profiles))

    if [ ${#available_profiles[@]} -eq 0 ]; then
      echo "Error: No AWS profiles configured."
      echo ""
      echo "Please configure AWS credentials:"
      echo ""
      echo "For SSO:"
      echo "  aws configure sso"
      echo ""
      echo "For standard credentials:"
      echo "  aws configure"
      echo ""
      echo "Or visit: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html"
      exit 1
    elif [ ${#available_profiles[@]} -eq 1 ]; then
      AWS_PROFILE="${available_profiles[0]}"
      echo "Using AWS profile: $AWS_PROFILE"
      echo ""
    else
      AWS_PROFILE=$(select_aws_profile "${available_profiles[@]}")
      echo ""
      echo "Using AWS profile: $AWS_PROFILE"
      echo ""
    fi

    # Export for caller script to use
    export AWS_PROFILE
  fi

  # Set aws_cmd with profile
  if [ -n "$AWS_PROFILE" ]; then
    profile_flag="--profile $AWS_PROFILE"
    aws_cmd="aws $profile_flag"
  fi

  # Check if SSO profile and handle SSO login
  if is_sso_profile "$AWS_PROFILE"; then
    echo "Detected SSO profile. Checking SSO session..."
    echo ""

    # Test SSO session with sts call
    local test_result=$(eval "$aws_cmd sts get-caller-identity 2>&1")
    local test_code=$?

    if [ $test_code -ne 0 ]; then
      if echo "$test_result" | grep -q "SSO\|sso\|Token"; then
        echo "SSO session expired. Running 'aws sso login'..."
        echo ""
        aws sso login --profile "$AWS_PROFILE"
        echo ""
      fi
    fi
  fi

  # Test credentials with actual API call
  echo "Checking AWS credentials..."
  echo ""

  CALLER_IDENTITY=$(eval "$aws_cmd sts get-caller-identity 2>&1")
  RESULT_CODE=$?

  if [ $RESULT_CODE -ne 0 ]; then
    echo "Error: AWS credentials are not configured or are invalid."
    echo ""
    echo "Error details:"
    echo "$CALLER_IDENTITY"
    echo ""
    echo "Would you like to configure AWS credentials now? (yes/no)"
    read -p "> " configure_now

    if [ "$configure_now" = "yes" ]; then
      echo ""
      echo "Running AWS configuration..."
      echo ""

      if [ -n "$AWS_PROFILE" ]; then
        echo "Configuring profile: $AWS_PROFILE"
        aws configure --profile "$AWS_PROFILE"
      else
        aws configure
      fi

      # Re-test credentials
      echo ""
      echo "Testing credentials..."
      CALLER_IDENTITY=$(eval "$aws_cmd sts get-caller-identity 2>&1")
      RESULT_CODE=$?

      if [ $RESULT_CODE -ne 0 ]; then
        echo ""
        echo "Error: Credentials still not working."
        echo "Please check your configuration and try again."
        echo ""
        echo "You can manually configure AWS credentials by running:"
        if [ -n "$AWS_PROFILE" ]; then
          echo "  aws configure --profile $AWS_PROFILE"
        else
          echo "  aws configure"
        fi
        exit 1
      fi
    else
      echo ""
      echo "Please configure AWS credentials before running this script:"
      if [ -n "$AWS_PROFILE" ]; then
        echo "  aws configure --profile $AWS_PROFILE"
      else
        echo "  aws configure"
      fi
      echo ""
      echo "Or set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
      exit 1
    fi
  fi

  # Success - print caller identity for verification
  echo "AWS credentials verified!"

  # Parse and display key info
  if command -v jq > /dev/null 2>&1; then
    ACCOUNT=$(echo "$CALLER_IDENTITY" | jq -r '.Account')
    ARN=$(echo "$CALLER_IDENTITY" | jq -r '.Arn')
    echo "  Account: $ACCOUNT"
    echo "  Identity: $ARN"
  else
    # Fallback without jq
    ACCOUNT=$(echo "$CALLER_IDENTITY" | grep -o '"Account"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"Account"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
    if [ -n "$ACCOUNT" ]; then
      echo "  Account: $ACCOUNT"
    fi
  fi

  echo ""

  return 0
}
