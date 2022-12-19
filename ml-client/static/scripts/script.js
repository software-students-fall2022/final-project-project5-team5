contentImageInput.onchange = e => {
    contentImg.src = URL.createObjectURL(contentImageInput.files[0]);  
    console.log(contentImg.src)
  };

styleImageInput.onchange = e => {
    styleImg.src = URL.createObjectURL(styleImageInput.files[0]);
    console.log(styleImg.src)
};

function uploadStyleImage(){
    document.getElementById("styleImageInput").click();
}

function uploadContentImage(){
    document.getElementById("contentImageInput").click();
}


async function getImages() {
    document.getElementById("contentImageURI").value = await new Promise(resolve => {
        let reader = new FileReader();
        try {
            reader.readAsDataURL(contentImageInput.files[0]);
        }
        catch {
            resolve("Content Image Error")
        }
        reader.onload = () => resolve(reader.result);
    });
    console.log(document.getElementById("contentImageURI").value)
    document.getElementById("styleImageURI").value = await new Promise(resolve => {
        let reader = new FileReader();
        try {
            reader.readAsDataURL(styleImageInput.files[0]);
        }
        catch {
            resolve("Style Image Error")
        }
        reader.onload = () => resolve(reader.result);
    });
    console.log(document.getElementById("styleImageURI").value)
    document.getElementById("uploadForm").submit()

}

function timeCompleted() {
    let currentTime = JSON.parse(localStorage.getItem("counter"));
    currentTime += 1;
    localStorage.setItem("counter", JSON.stringify(currentTime));
}

// start timer when generator button clicked
document.getElementById("generateImg").addEventListener("click", function() {
    let counter = 0;
    localStorage.setItem("counter", JSON.stringify(counter));
    let start = setInterval(timeCompleted, 1000);
});

function getTime(){
    let currentTime = JSON.parse(localStorage.getItem("counter"));
            if (currentTime > 60) {
                let mins = Math.floor(currentTime / 60);
                let seconds = time - mins * 60;
                document.getElementById("totalTime").innerText = `Total time to create stylized image: ${mins} mins ${seconds} secs`;
            } else if(currentTime != 0 ) {
                document.getElementById("totalTime").innerText = `Total time to create stylized image: ${currentTime} seconds`;
            }
}