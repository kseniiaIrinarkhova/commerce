# commerce
Project2: commerce CS50w

# Distinctiveness and Complexity
Current  commerce web site could provide you opportunity to create a listing, check new bids and comments on it, add listings from other users to your watch list, place your own bids in interesting listings and add new comments. You have all information about your own listings in "My listing" page and about interesting for you listings in "Watch list" page. You could simply add new listing or edit the existing one that you created earlier. 
It is easy to customize the UI of this commerce web site, because initially it uses all benefits of bootstrap 5 framework. The logic of this commerce web site is simple and clear which prevent all kinds of technical issues. Usage of such fitures as login_required Django decorators secure this web site from unauthorized access. For the purpose of convenuent UI this program uses the feature of custom widgets for providing opportunity to user at the same time choose or create new categories for listing items.  
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
    Class represents comments for listing. Contains: link for context  (foreign key for Listing), link for author (foreign key for User), and Text
- **Category**
    Class represents listing's category. It conteins of category's title.
### HTML templates and static files
- **Changes in HTML templates and static files**
- - *index.html*
    Provided information of all active listings 
- - *layout.html*
    Added links for creation new listing, Watch List, My listings, Edit page 
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
- ```path("listing/<int:listing_id>/place_bid", views.place_bid, name="place_bid")``` path for placing bid function
- ```path("listing/<int:listing_id>/close_auction", views.close_auction, name="close_auction")``` path for closing auction function
- ```path("listing/<int:listing_id>/add_comment", views.add_comment, name="add_comment")``` path for adding comment function
### Changes in __views.py__
- changings in **index** view
Added list of active listings to the view.
- changes in **register** view
Added information about First and Last user names.
- **listing** view
Provided information for listing page. Checked if user authorized then provide information what user could bo with listing. Provide informationa about all comments that listing has.
- **new_listing** view
Showed algorithm of creation a new listing, render to editor.html with attributes:
- - *title* - title for editor's page, by default is "New listing"
- - *action* - action is ```new_listing```
- - *listing_id* - is None as it is cteation of a new listing
- - *form* - form based on ListingForm() class
Authorization is requeired for this view.
- **my_listings** view
Showed information of all listings that belong to the user. Rendered to ```owner_list.html``` with parameters:
- - *active_list* - list of active listings
- - *closed_list* - list of closed listings
Authorization is requeired for this view.
- **edit** view
Provided algorithm of listing's editing, render to editor.html with attributes:
- - *title* - title for editor's page, includes listing title 
- - *action* - action is ```edit```
- - *listing_id* - primary key of listing that would be edited
- - *form* - form based on ListingForm() class with instance of Listing model and initial value for ```categoryTitle``` from category of chosen listing
Authorization is requeired for this view.
- **edit_watchlist** view
Provided algorithm of adding listing to user's watch list or deleting from it. After changings render back to listing page. Authorization is requeired for this view.
- **my_watchlist** view
Showed information about listings that are in user's watch list. Rendered to ```watchlist.html``` with parameters:
- - *active_list* - list of active listings
- - *closed_list* - list of closed listings
Authorization is requeired for this view.
- **place_bid** view
Provide algorithm of placing the bid in listing page. Checked if bid could be placed and return the imformation of successful bid or about some errors. Rendered to ```listing.html```. Authorization is requeired for this view.
- **close_auction** view
Provide algorithm of closing the auction for the chosen listing. Rendered to ```listing.html```. Authorization is requeired for this view.
- **add_comment** view
Provide algorithm of adding comment to the listing. Rendered to ```listing.html```. Authorization is requeired for this view.
### Changes in __utils.py__
- **ListTextWidget(forms.TextInput)** class
Class inherited from form.TextInput class. Used to create customs widget for textinput with provided values as ```<dalalist> <option>```
- **ListingForm(ModelForm)** Class
Class inherited from ModelForm based on ```Listing``` model
- **BidForm(ModelForm)** Class
Class inherited from ModelForm based on ```Bid``` model 
- **getCategory(categoryTitle)** function
Returns ```Category``` model from category title if category existed or create new category.
- **getWatchListAction(listing_id, user)** function
Returns type of action that could be provided to user: add listing to user's watch list, or delete this listing from it.
- **checkNewBid(new_bid, listing_id)** function
Returns the result of checking if new bid higher than existing ones or higher than or equel to the listing price.
## Installation
To install the current project locally user should download the whole code from the current repository, then in the terminal run a command:
```python manage.py  runserver```. After that action user could find the server path in `Starting development server at <<provided path>>` line. Then the user may click, copy or text this `<<provided path>>` in a browser. 
superuser info: admin (CS50w-2023)
## User guide
Without authorization user have an oppotrunity to visit:
- index page and see all active listings
- listing page and see detailed information about the listing and comments
- login page 
- registration page
After login/registration user is able to:
1. in listing page:
- place/remove listing to/from his/her watch list if it is not his/her listing
- add comment to listing
- place a bid for current listing if it is not his/her listing
- close the auction if he/she is listing owner
- edit his/her listing by chosing "Edit" menu
2. visit "Watch List" page to see all active and closed listings that he/she placed in watch list. User could delete listing from watch list in this page or go directly to the listing page.
3. create a new listing by chosing "Create new listing" menu. User should add listing title, listing price and could add listing description, url for listing image and listing category. User is able to chose listing category from drop down list or add a new one.
4. visit "My listings" page to see all active and closed his/her listings with information about bids. User could edit his/her listing or close the auction for any of his/her active listings.

