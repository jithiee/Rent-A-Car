 
 const hamburgerButton = document.getElementById('hamburger-button');
        const mobileMenu = document.getElementById('mobile-menu');
        const mainNavbar = document.getElementById('main-navbar'); // Get the main navbar element

        // Function to close the menu
        function closeMobileMenu() {
            if (!mobileMenu.classList.contains('hidden')) { // Only close if it's open
                mobileMenu.classList.add('hidden');
                hamburgerButton.classList.remove('hamburger-active');
            }
        }

        // Toggle the menu when hamburger button is clicked
        hamburgerButton.addEventListener('click', (event) => {
            event.stopPropagation(); // Prevent this click from propagating to the document listener immediately
            mobileMenu.classList.toggle('hidden');
            hamburgerButton.classList.toggle('hamburger-active');
        });

        // Close the menu when clicking outside of the navbar (including the mobile menu)
        document.addEventListener('click', (event) => {
            // Check if the clicked target is NOT within the main navbar
            if (!mainNavbar.contains(event.target)) {
                closeMobileMenu();
            }
        });

        // Optional: Close menu when a link inside it is clicked (common UX)
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                closeMobileMenu();
            });
        });

        // Close menu on resize if it's open (good for transitioning between mobile/desktop view)
        window.addEventListener('resize', () => {
            if (window.innerWidth >= 768) { // 768px is Tailwind's 'md' breakpoint
                closeMobileMenu();
            }
        });


    

        
      
        