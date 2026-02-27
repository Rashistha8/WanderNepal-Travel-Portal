// Wanderlust Premium Interactions
document.addEventListener('DOMContentLoaded', function() {
    
    // Smooth Scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            target?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });

    // Navbar Scroll Effect
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('nav');
        if (window.scrollY > 50) {
            navbar?.classList.add('shadow-lg', 'backdrop-blur-md');
        } else {
            navbar?.classList.remove('shadow-lg', 'backdrop-blur-md');
        }
    });

    // Category Filter Animation
    document.querySelectorAll('[data-category]').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('[data-category]').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Smooth fade out/in
            document.querySelector('.grid')?.classList.add('opacity-0');
            setTimeout(() => {
                window.location.href = `?category=${this.dataset.category}`;
            }, 200);
        });
    });

    // Card Hover Animations
    document.querySelectorAll('.group').forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-8px) scale(1.02)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Booking Button Loading
    document.querySelectorAll('form[method="POST"]').forEach(form => {
        form.addEventListener('submit', function() {
            const btn = this.querySelector('button[type="submit"]');
            btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Booking...';
            btn.disabled = true;
        });
    });

    // Intersection Observer for Fade-in
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    });

    document.querySelectorAll('.fade-in-up').forEach(el => observer.observe(el));
});

// Parallax Hero Effect
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero-section');
    if (hero) {
        hero.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
});
