// Animasi saat hover
document.querySelector('.card').addEventListener('mouseover', function() {
    this.style.transform = 'scale(1.05) rotate(2deg)';
    this.style.transition = 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out';
    this.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.2)';
});

document.querySelector('.card').addEventListener('mouseout', function() {
    this.style.transform = 'scale(1) rotate(0deg)';
    this.style.boxShadow = 'none';
});

// Alert saat halaman dimuat
window.addEventListener('load', () => {
    console.log('Website siap digunakan!');
});
