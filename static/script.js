// Animasi saat hover
document.querySelector('.card').addEventListener('mouseover', function() {
    this.style.transform = 'scale(1.02)';
    this.style.transition = 'transform 0.3s';
});

document.querySelector('.card').addEventListener('mouseout', function() {
    this.style.transform = 'scale(1)';
});

// Alert saat halaman dimuat
window.addEventListener('load', () => {
    console.log('Website siap digunakan!');
});