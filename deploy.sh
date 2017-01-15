#!/bin/bash
# Deploy to S3
s3cmd sync --delete-removed \
    --exclude '.git/*' \
    --rexclude "^(.*\.((html|xml|json)$))*$" \
    --add-header="Cache-Control: max-age=1440" \
    --acl-public \
    --preserve \
    --no-mime-magic \
    --guess-mime-type \
    --recursive \    
    public/ \
    s3://$1/ 
s3cmd sync --delete-removed \
    --exclude '*' \
    --rinclude "^(.*\.((html|xml|json)$))*$" \
    --add-header="Cache-Control: no-cache, no-store, must-revalidate" \
    --add-header="Pragma: no-cache" \
    --add-header="Expires: 0" \
    --acl-public \
    --preserve \
    --no-mime-magic \
    --guess-mime-type \
    --recursive \
    public/ \
    s3://$1/ 
# Purge CDN Cache
curl \"https://api.keycdn.com/zones/purge/$2.json\" -u $3:"