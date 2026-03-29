document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Fungsi Klik Opsi Tes Minat dengan Selection
    const optionButtons = document.querySelectorAll('.btn-option');
    optionButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            // Hapus kelas selected dari saudara-saudaranya dalam group yang sama
            const parentCard = this.closest('.tes-card-full');
            if (parentCard) {
                parentCard.querySelectorAll('.btn-option').forEach(el => {
                    el.classList.remove('selected');
                });
            }
            
            // Tambah kelas selected pada yang diklik
            this.classList.add('selected');
            
            // Set value ke hidden input
            const inputName = this.getAttribute('data-name');
            const inputValue = this.getAttribute('data-value');
            const hiddenInput = document.getElementById('input_' + parentCard.getAttribute('data-question'));
            
            if (hiddenInput) {
                hiddenInput.value = inputValue;
            }
            
            // Update progress bar
            updateProgressBar();
        });
    });

    // 2. Progress Bar Animation untuk Tes Minat
    function updateProgressBar() {
        const progressBar = document.getElementById('progressBar');
        if (!progressBar) return;
        
        const tesCards = document.querySelectorAll('.tes-card-full');
        const totalQuestions = tesCards.length;
        let answeredQuestions = 0;
        
        tesCards.forEach(card => {
            const hiddenInput = card.querySelector('input[type="hidden"]');
            if (hiddenInput && hiddenInput.value) {
                answeredQuestions++;
            }
        });
        
        const progressPercentage = (answeredQuestions / totalQuestions) * 100;
        progressBar.style.width = progressPercentage + '%';
    }

    // 3. Radio Button Scale Enhancement untuk Tes Bakat
    const scaleLabels = document.querySelectorAll('.scale-label');
    scaleLabels.forEach(label => {
        label.addEventListener('click', function() {
            const input = this.querySelector('input[type="radio"]');
            if (input) {
                input.checked = true;
                
                // Visual feedback
                const parentCard = this.closest('.tes-card-full');
                if (parentCard) {
                    // Hapus highlight dari semua opsi dalam pertanyaan yang sama
                    parentCard.querySelectorAll('.scale-label .dot').forEach(dot => {
                        dot.style.transform = 'scale(1)';
                    });
                }
            }
        });
    });

    // 4. Fungsi Download / Cetak Hasil
    const btnDownload = document.querySelector('.btn-download');
    if (btnDownload) {
        btnDownload.addEventListener('click', (e) => {
            e.preventDefault();
            // Gunakan window.print() untuk cetak/save as PDF
            window.print();
        });
    }

    // 5. Smooth Scroll untuk Navigasi
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            const targetId = href.split('#')[1];
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                e.preventDefault();
                const offsetTop = targetElement.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // 6. Form Validation untuk Tes Minat
    const tesMinatForm = document.getElementById('tesMinatForm');
    if (tesMinatForm) {
        tesMinatForm.addEventListener('submit', function(e) {
            const hiddenInputs = tesMinatForm.querySelectorAll('input[type="hidden"]');
            let allAnswered = true;

            hiddenInputs.forEach(input => {
                if (!input.value) {
                    allAnswered = false;
                }
            });

            if (!allAnswered) {
                e.preventDefault();
                alert('Mohon jawab semua pertanyaan sebelum submit!');
                return false;
            }
        });
    }
    
    // Form Validation untuk Tes Bakat
    const tesBakatForm = document.getElementById('tesBakatForm');
    if (tesBakatForm) {
        tesBakatForm.addEventListener('submit', function(e) {
            const radioGroups = tesBakatForm.querySelectorAll('input[type="radio"]');
            const groupNames = new Set();
            const answeredGroups = new Set();
            
            radioGroups.forEach(radio => {
                groupNames.add(radio.name);
                if (radio.checked) {
                    answeredGroups.add(radio.name);
                }
            });
            
            if (groupNames.size !== answeredGroups.size) {
                e.preventDefault();
                alert('Mohon jawab semua pertanyaan sebelum submit!');
                return false;
            }
        });
    }

    // 7. Auto-hide Flash Messages
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });

    // 8. Animasi untuk Cards saat Scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe cards and test cards
    document.querySelectorAll('.card, .test-card, .work-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease';
        observer.observe(el);
    });
});

// CSS untuk animasi slideOut
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);