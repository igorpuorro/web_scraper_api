// Create a global variable to store the return value
let openedWindow;
let openedUrl;

(function () {
    // Save a reference to the original window.open function
    const originalWindowOpen = window.open;

    // Override the window.open function
    window.open = function (url, target, features) {
        // Check if the 'target' parameter is '_blank' (opens in a new tab/window)
        if (target === '_blank') {
            // Call the original window.open function to open the new tab
            openedWindow = originalWindowOpen.apply(this, arguments);

            openedUrl = url

            // You can add your monitoring function here
            console.log('New tab was opened with URL:', url);

            return openedWindow;
        }

        // If 'target' is not '_blank', open the link in the same tab/window
        return window.location.href = url;
    };

    // Find and add click event listeners to all <a> tags
    const links = document.querySelectorAll('a');

    links.forEach(link => {
        link.addEventListener('click', function (event) {
            // Check if the link opens in a new tab/window
            if (link.getAttribute('target') === '_blank') {
                // You can add your monitoring function here
                console.log('Link with target="_blank" was clicked:', link.href);
            }
        });
    });
})();
