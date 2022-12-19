contentImageInput.onchange = e => {
    contentImg.src = URL.createObjectURL(contentImageInput.files[0]);  
  };

styleImageInput.onchange = e => {
    styleImg.src = URL.createObjectURL(styleImageInput.files[0]);
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
    document.getElementById("spinDiv").classList.remove("hidden");
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

let classical = document.getElementById("classical")
let realist = document.getElementById("realist")
let romantic = document.getElementById("romantic")
let impressionist = document.getElementById("impressionist")
let modern = document.getElementById("modern")
let misc = document.getElementById("misc")
let styleInput = document.getElementById("imageStyle")

styles = [classical, realist, romantic, impressionist, modern, misc];

function toggleStyles(selectedStyle){
    for(let i=0; i < styles.length; i++){
        if(styles[i] !== selectedStyle && styles[i].classList.contains("active")){
            styles[i].classList.toggle("active")
        }
    }
}


classical.addEventListener("click", function() {
    classical.classList.toggle("active");
    if(classical.classList.contains("active")){
        toggleStyles(classical);
        styleInput.value="classical";
    }
    else {
        styleInput.value="";
    }
})

realist.addEventListener("click", function() {
    realist.classList.toggle("active");
    if(realist.classList.contains("active")){
        toggleStyles(realist);
        styleInput.value="realist";
    }
    else {
        styleInput.value="";
    }
})

romantic.addEventListener("click", function() {
    romantic.classList.toggle("active");
    if(romantic.classList.contains("active")){
        toggleStyles(romantic);
        styleInput.value="romantic";
    }
    else {
        styleInput.value="";
    }
})

impressionist.addEventListener("click", function() {
    impressionist.classList.toggle("active");
    if(impressionist.classList.contains("active")){
        toggleStyles(impressionist);
        styleInput.value="impressionist";
    }
    else {
        styleInput.value="";
    }
})

modern.addEventListener("click", function() {
    modern.classList.toggle("active");
    if(modern.classList.contains("active")){
        toggleStyles(modern);
        styleInput.value="modern";
    }
    else {
        styleInput.value="";
    }
})

misc.addEventListener("click", function() {
    misc.classList.toggle("active");
    if(misc.classList.contains("active")){
        toggleStyles(misc);
        styleInput.value="misc";
    }
    else {
        styleInput.value="";
    }
})