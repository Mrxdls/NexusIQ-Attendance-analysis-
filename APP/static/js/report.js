// report.js - JavaScript functionality for the report page

document.addEventListener('DOMContentLoaded', function() {
    // Animation on scroll for report elements
    const animateElements = document.querySelectorAll('.feature-card, .stat-item, .download-btn, .action-btn, .preview-image');
    
    // Add initial opacity to elements for smooth animation
    animateElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });
    
    // Animate elements when they enter the viewport
    function animateOnScroll() {
        animateElements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight;
            
            if(elementPosition < screenPosition - 100) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    }
    
    // Run animation check on initial load and scroll
    animateOnScroll();
    window.addEventListener('scroll', animateOnScroll);
    
    // Add interactive hover effects for preview images
    const previewImages = document.querySelectorAll('.preview-image');
    
    previewImages.forEach(image => {
        image.addEventListener('mouseover', function() {
            image.style.transform = 'scale(1.05) translateZ(0)';
            image.style.zIndex = '10';
            image.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.2)';
            image.style.transition = 'all 0.3s ease';
        });
        
        image.addEventListener('mouseout', function() {
            image.style.transform = '';
            image.style.zIndex = '';
            image.style.boxShadow = '';
        });
    });
    
    // Add floating animation to download buttons
    const downloadButtons = document.querySelectorAll('.download-btn');
    let animationDirection = 1;
    
    function floatAnimation() {
        downloadButtons.forEach((button, index) => {
            setTimeout(() => {
                button.style.transform = `translateY(${-5 * animationDirection}px)`;
                button.style.transition = 'transform 1.5s ease-in-out';
            }, index * 150);
        });
        
        animationDirection *= -1;
    }
    
    // Run floating animation every 2 seconds
    setInterval(floatAnimation, 2000);
    floatAnimation(); // Initial animation
    
    // Display notification when download buttons are clicked
    downloadButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Prevent default only for demo purposes - remove this line when actual download functionality is implemented
            // e.preventDefault();
            
            // Create notification
            const notification = document.createElement('div');
            notification.className = 'download-notification';
            notification.innerHTML = `<i class="fas fa-check-circle"></i> Your report is being prepared for download!`;
            
            // Style the notification
            notification.style.position = 'fixed';
            notification.style.bottom = '20px';
            notification.style.right = '20px';
            notification.style.backgroundColor = '#28a745';
            notification.style.color = 'white';
            notification.style.padding = '15px 25px';
            notification.style.borderRadius = '8px';
            notification.style.boxShadow = '0 5px 15px rgba(0,0,0,0.2)';
            notification.style.zIndex = '1000';
            notification.style.transform = 'translateY(100px)';
            notification.style.transition = 'transform 0.3s ease';
            
            // Add to body
            document.body.appendChild(notification);
            
            // Show notification
            setTimeout(() => {
                notification.style.transform = 'translateY(0)';
            }, 10);
            
            // Remove notification after 3 seconds
            setTimeout(() => {
                notification.style.transform = 'translateY(100px)';
                setTimeout(() => {
                    document.body.removeChild(notification);
                }, 300);
            }, 3000);
        });
    });
});