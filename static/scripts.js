document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("file");
    fileInput.addEventListener("change", () => {
        if (fileInput.files.length > 0) {
            alert(`Вы выбрали файл: ${fileInput.files[0].name}`);
        }
    });
});
