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
- - *index.html*
    Provided information of all active listings 
- - *layout.html*
    Added links for creation new listing, Watch List, My listings 
- **New HTML templates**
- - *listing.html*
    Provide detailed information about listing. Provide information about bids and comments
- - *editor.html*
    Provide template for creation a new listing or editing existing listing  
- - *owner_list.html*
    Provide lists for active and closed listing that user posted
- - *watchlist.html*
    Provide lists for active and closed listing that user added to watchlist
- **Changes in static files**
- - *img* folder
    Folder for images that are used in website styles
- - *styles.css* file
    All information about CSS.
### Changes in __urls.py__
File __urls.py__ provided information about all paths in application. Additional list of paths provided below.
- ```path("listing/<int:listing_id>", views.listing, name="listing")``` path for listing item
- ```path("listing/new", views.new_listing, name="new_listing")``` path for creation new listing item
- ```path("listing/mine", views.my_listings, name="my_listings")``` path for owner list
- ```path("listing/watchlist", views.my_watchlist, name="my_watchlist")``` path for watchlist
- ```path("listing/<int:listing_id>/edit", views.edit, name="edit")``` path for listing editor
- ```path("listing/<int:listing_id>/edit_watchlist", views.edit_watchlist, name="edit_watchlist")``` path for adding items to watchlist or excluding them from it
### Changes in __views.py__
- changings in **index** view
Added list of active listings to the view.
- **listing** view
Provided information for listing page. Additionally provide statuses of listing:
- - *is_editable* - if the owner open the listing, it could be editable 
- - *is_watchable* - provide information that the listing could be added to watch list or deleted from itis_in_watchlist
- - *is_in_watchlist* - provide information that the user has this listing in his/her watch list
- **new_listing** view
Showed algorithm of creation a new listing, render to editor.html with attributes:
- - *title* - title for editor's page, by default is "New listing"
- - *action* - action is ```new_listing```
- - *listing_id* - is None as it is cteation of a new listing
- - *form* - form based on ListingForm() class
To be able doing providing actions user should be authorized.
- **my_listings** view
Showed information of all listings that belong to the user. Rendered to ```owner_list.html``` with parameters:
- - *active_list* - list of active listings
- - *closed_list* - list of closed listings
To be able doing providing actions user should be authorized.
- **edit** view
Provided algorithm of listing's editing, render to editor.html with attributes:
- - *title* - title for editor's page, includes listing title 
- - *action* - action is ```edit```
- - *listing_id* - primary key of listing that would be edited
- - *form* - form based on ListingForm() class with instance of Listing model and initial value for ```categoryTitle``` from category of chosen listing
To be able doing providing actions user should be authorized.
- **edit_watchlist** view
Provided algorithm of adding listing to user's watch list od deleting from it. After changings render back to listing page. To be able doing providing actions user should be authorized.
- **my_watchlist** view
Showed information about listings that are in user's watch list. Rendered to ```watchlist.html``` with parameters:
- - *active_list* - list of active listings
- - *closed_list* - list of closed listings
To be able doing providing actions user should be authorized.
### Changes in __utils.py__
- **ListTextWidget(forms.TextInput)** class
Class inherited from form.TextInput class. Used to create customs widget for textinput with provided values as ```<dalalist> <option>```
- **ListingForm(ModelForm)** Class
Class inherited from ModelForm based on ```Listing``` model
- **getCategory(categoryTitle)** function
Returns ```Category``` model from category title.
- **getWatchListAction(listing_id, user)** function
Returns type of action that could be provided to user: add listing to user's watch list, or delete this listing from it
## Installation
## User guide
superuser: admin (CS50w-2023)