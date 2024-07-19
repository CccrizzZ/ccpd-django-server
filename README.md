# CCPD Django Cloud Controller
<div>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
<img src="https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white" />
<img src="https://img.shields.io/badge/Microsoft_Azure-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white" />
</div>

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%203.svg)](https://www.digitalocean.com/?refcode=3b0d0ab4927b&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)

## Services
- Q&A inventory form controller.
- Inventory image gallery controller.
    - Upload and download image from Microsoft Azure.
    - User gallery for manipulate images.
- User authentication controller.
    - Routes for different roles
- Admin controller contains admin only functions.
    - Full control over Q&A user group information.
    - Full control over Q&A inventory information.
    - Convert Q&A record to actual listable inventory.
    - Manage retail and return inventory.

## Commands
```
# Start local development server
python manage.py runserver

# Run deployment check
python manage.py check --deploy

# Generate requirement.txt
pip freeze > requirements.txt
```

