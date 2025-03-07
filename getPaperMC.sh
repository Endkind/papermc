#!/bin/bash
VERSION=$(cat /endkind/papermc_version)
BASE_URL="https://api.papermc.io/v2/projects/paper"

if [ $VERSION == "latest" ]; then
  VERSION=$(curl -s "$BASE_URL" | jq -r '.versions | .[-1]')
fi

LATEST_BUILD=$(curl -s "$BASE_URL/versions/$VERSION" | jq -r '.builds | .[-1]')

curl -o "/endkind/server.jar" -L "$BASE_URL/versions/$VERSION/builds/$LATEST_BUILD/downloads/paper-$VERSION-$LATEST_BUILD.jar"
if [ $? -eq 0 ]; then
  echo "Download PaperMC Version ($VERSION) Build ($LATEST_BUILD)"
else
  echo "An error occurred while downloading PaperMC. Please try again or recreate the container."
  exit 1
fi
