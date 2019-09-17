#!/bin/bash
# ./createStack.sh <aws_account_id> <aws_profile_name> <aws_region> <stack_name>

AWS_ACCOUNT_ID=$1
AWS_PROFILE_NAME=$2
AWS_REGION=$3
STACK_NAME=$4
CLOUD_FORMATION_RESOURCE_UPLOAD_BUCKET_NAME="cloudformation-uploads-$AWS_ACCOUNT_ID"

RELEASE_ID=$RANDOM
CHANGE_SET_NAME="changeset-$RELEASE_ID"
CHANGE_SET_TYPE="CREATE"

#Packing code
# Preparing lambda dependencies
pip3 install --target ./package requests jinja2
cd package
zip -r9 ${OLDPWD}/prober.py.zip .
cd $OLDPWD
zip -r9 prober.py.zip static
zip -g prober.py.zip prober.py

aws s3 mb --profile $AWS_PROFILE_NAME --region $AWS_REGION s3://$CLOUD_FORMATION_RESOURCE_UPLOAD_BUCKET_NAME 2> /dev/null

aws s3 cp template.json s3://$CLOUD_FORMATION_RESOURCE_UPLOAD_BUCKET_NAME/$STACK_NAME/template.json --profile $AWS_PROFILE_NAME
aws s3 cp "policy/policy.json" s3://$CLOUD_FORMATION_RESOURCE_UPLOAD_BUCKET_NAME/$STACK_NAME/"policy.json" --profile $AWS_PROFILE_NAME
aws s3 cp prober.py.zip s3://$CLOUD_FORMATION_RESOURCE_UPLOAD_BUCKET_NAME/$STACK_NAME/prober.py.zip --profile $AWS_PROFILE_NAME


echo "Create change set: $CHANGE_SET_NAME"
aws cloudformation create-change-set \
    --change-set-name $CHANGE_SET_NAME \
	--change-set-type $CHANGE_SET_TYPE \
    --profile $AWS_PROFILE_NAME \
    --region $AWS_REGION \
    --stack-name $STACK_NAME \
    --template-url "https://s3-$AWS_REGION.amazonaws.com/$CLOUD_FORMATION_RESOURCE_UPLOAD_BUCKET_NAME/$STACK_NAME/template.json" \
    --capabilities CAPABILITY_NAMED_IAM


echo "Wait for change set to be created: $CHANGE_SET_NAME"
aws cloudformation wait change-set-create-complete --stack-name=$STACK_NAME --change-set-name=$CHANGE_SET_NAME --profile=$AWS_PROFILE_NAME --region=$AWS_REGION

read -p "Press any key"

echo "Execute change set: $CHANGE_SET_NAME"
aws cloudformation execute-change-set --stack-name=$STACK_NAME --change-set-name=$CHANGE_SET_NAME --profile=$AWS_PROFILE_NAME --region=$AWS_REGION

echo 'Deployment finished'
rm -f prober.py.zip
echo 'Zip file removed'