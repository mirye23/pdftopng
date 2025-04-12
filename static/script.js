// script.js

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("upload-form");
    const downloadSection = document.getElementById("download-section");
    const downloadLink = document.getElementById("download-link");

    form.addEventListener("submit", function (e) {
        e.preventDefault(); // 기본 동작 막기

        const fileInput = document.getElementById("pdf-file");
        const file = fileInput.files[0];

        if (!file) {
            alert("PDF 파일을 선택해주세요.");
            return;
        }

        const formData = new FormData();
        formData.append("pdf_file", file);

        fetch("/convert", {
            method: "POST",
            body: formData,
        })
        .then(async (response) => {
            if (!response.ok) {
                const error = await response.text();
                throw new Error(error || "변환에 실패했습니다.");
            }
            return response.blob();
        })
        .then((blob) => {
            const url = window.URL.createObjectURL(blob);
            downloadLink.href = url;
            downloadLink.download = "converted.jpg";
            downloadSection.style.display = "block";
        })
        .catch((error) => {
            alert("에러 발생: " + error.message);
            console.error("변환 에러:", error);
        });
    });
});
