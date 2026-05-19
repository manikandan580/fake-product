// Example: Confirm before submitting upload
document.addEventListener("DOMContentLoaded", function() {
    const uploadForm = document.querySelector("form");
    if(uploadForm) {
        uploadForm.addEventListener("submit", function(e) {
            const confirmUpload = confirm("Are you sure you want to upload this product?");
            if(!confirmUpload) e.preventDefault();
        });
    }
});