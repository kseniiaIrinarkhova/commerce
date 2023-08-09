# commerce
Project2: commerce CS50w

# Distinctiveness and Complexity

# Technical documentation of the project
## Code specification
### Models description
Basic model structure for current project provided below:
- **User**
    Class that provided information about users, based on AbstractUser class. Included addition many to many connection to Listing class, that showed WatchList of items for user.
- **Listing**
    Class represent object of listing. Contains: title, description, price, url for image, link for category (foreign key for Category ), information about auctioneer (foreign key for User), and information is listiong active or not.
- **Bid**
    Class provides information about bids. Includes: link for bidder(foreign key for User), link for context (foreign key for Listing), and bid's price.
- **Comment**
    Class represents comments for listing. Contains: link for context  (foreign key for Listing), link for author (foreign key for User), Text, count of likes, count of dislikes
- **Category**
    Class represents listing's category. It conteins of category's title.
### HTML templates and static files
- **Changes in HTML templates and static files**
- **New HTML templates**
### Changes in __urls.py__
### Changes in __views.py__

## Installation
## User guide
superuser: admin (CS50w-2023)