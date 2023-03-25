# Custom Wallpaper in Firefox 

Personalize your Firefox browser's home page, new tab, and private browsing tab with this custom background and styling project. It alters the appearance of certain elements on these pages and adds a custom background image to enhance your browsing experience.

## Installation

1. Clone this repository into your Firefox profile's `chrome` folder. If the `chrome` folder does not exist, create one. To find the Firefox profile, visit `about:support` in your Firefox browser. Click the `Open Directory` button to access the profile folder.


2. Locate the `userContent.css` file in the `chrome` folder (create one if it doesn't exist). Then, import the `wallpaper.css` file by adding the following line:

@import url("firefox_wallpaper/wallpaper.css");


3. Add your desired background image to the `img` folder and name it `city.jpg`. If you prefer a different file name or format, update the CSS code accordingly.

4. Visit `about:config` and set the `toolkit.legacyUserProfileCustomizations.stylesheets` setting to `true`.

5. Restart Firefox to see the custom styling in effect.

## Example
![Alt text](https://github.com/GabrielTorland/firefox_wallpaper/example.png "Firefox Homepage")
