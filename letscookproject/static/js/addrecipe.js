let ingredient_name_input = document.querySelector("#ingredient_name_input") 
let ingredient_quantity_input = document.querySelector("#ingredient_quan_input") 
let add_bt = document.querySelector(".add_ingredient")
let ingredients_data = document.querySelector(".ingredients_data")
let recipe_id = document.querySelector("#recipe_id").value;
let csrf_token = document.querySelector("#csrf_token").value;
let removeIcon = document.querySelector("#remove_icon_url").value;
let input_img  = document.querySelector(".input_img")
let display_image = document.querySelector(".recipe_image")
let add_recipe_bt = document.querySelector("#add_recipe_bt")
let recipe_name_input = document.querySelector(".take_input")
let select_course = document.querySelector(".select_course")
let ingredients_contaier = document.querySelector(".ingredients")
let ingredient_Arr = document.querySelectorAll(".ingredient")

input_img.addEventListener("change", function(event) {
    const file = event.target.files[0]; 
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const imageUrl = e.target.result;
            console.log(e.target.result);
            display_image.style.backgroundImage = `url('${imageUrl}')`;
            image_url = imageUrl;
        };
        reader.readAsDataURL(file);
    } 
    document.querySelector(".upload_icon").classList.add("none")
   
});

add_bt.addEventListener("click", function(e){
    e.preventDefault(); 
    if (check_valid_ingredients()) {
        let name = ingredient_name_input.value;
        let amount = ingredient_quantity_input.value;

        fetch("/ajax/add-ingredient/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token
            },
            body: JSON.stringify({
                name: name,
                amount: amount,
                recipe_id: recipe_id
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                create_ingredient(data.ingredient_id)
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => {
            console.error("AJAX Error:", error);
        });
    }
});

function create_ingredient(id){

    let ingredient_name = ingredient_name_input.value;
    let ingredient_quantity = ingredient_quantity_input.value;
    if (!ingredient_name || !ingredient_quantity) return;
    
    let ingredient = document.createElement("div"); 
    ingredient.dataset.id = id;
    ingredient.innerHTML = `
        <div class="ingredient">
            <h1 class="ingredient_quan">x${ingredient_quantity}</h1>
            <h1 class="ingredient_name">${ingredient_name}</h1>
            <img src="${removeIcon}" class="remove">
        </div>
        <hr class="line">  
    `;
    ingredients_data.append(ingredient);
    let remove_bt = ingredient.querySelector(".remove");
    remove_bt.addEventListener("click", function () {
        const ingredientId = ingredient.dataset.id;
        fetch("/ajax/delete-ingredient/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token
            },
            body: JSON.stringify({ id: ingredientId })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                ingredient.remove();
            } else {
                alert("Error deleting ingredient");
            }
        });
    });


}


function check_valid_ingredients(){
    let NameTitleElement = ingredient_name_input.previousElementSibling;
    let QuanTitleElement = ingredient_quantity_input.previousElementSibling;
    let title_cont_Element = ingredients_contaier.previousElementSibling;
    let valid = true;
    if(!ingredient_name_input.value){
         NameTitleElement.classList.add("empty_title")
         ingredient_name_input.classList.add("empty_input");
         ingredients_contaier.classList.add("empty_input");
         title_cont_Element.classList.add("empty_title")
         valid=false;
         return
    }

    if(!ingredient_quantity_input.value){
        QuanTitleElement.classList.add("empty_title")
        ingredient_quantity_input.classList.add("empty_input");
        ingredients_contaier.classList.add("empty_input");
        title_cont_Element.classList.add("empty_title")
        valid=false;
        return
    }

    return valid;

}

function add_recipe(e){
    e.preventDefault();
    let all_done = true;
    let NameTitleElement = ingredient_name_input.previousElementSibling;
    let QuanTitleElement = ingredient_quantity_input.previousElementSibling;
    let title_cont_Element = ingredients_contaier.previousElementSibling;
    if(!recipe_name_input.value){
        let titleElement = recipe_name_input.previousElementSibling;
        titleElement.classList.add("empty_title")
        recipe_name_input.classList.add("empty_input");
        all_done = false;
    }

    if(!select_course.value){
        let titleElement = select_course.previousElementSibling;
        titleElement.classList.add("empty_title")
        select_course.classList.add("empty_input");
        all_done = false;
    }

    if(document.querySelectorAll(".ingredient").length == 0){
        NameTitleElement.classList.add("empty_title")
        ingredient_name_input.classList.add("empty_input");
         QuanTitleElement.classList.add("empty_title")
        ingredient_quantity_input.classList.add("empty_input");
        ingredients_contaier.classList.add("empty_input");
        title_cont_Element.classList.add("empty_title");
        all_done = false;
    }

    if (all_done) {
        document.querySelector(".add_product").submit();
    }
        
}


for(let i = 0 ; i < ingredient_Arr.length ; i++){
    let remove_bt = ingredient_Arr[i].querySelector(".remove");
    const ingredient = ingredient_Arr[i];
    remove_bt.addEventListener("click", function () {
        const ingredientId = ingredient.dataset.id;
         const line = ingredient.nextElementSibling;
        fetch("/ajax/delete-ingredient/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token
            },
            body: JSON.stringify({ id: ingredientId })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                ingredient.remove();
                line.remove();
            } else {
                alert("Error deleting ingredient");
            }
        });
    });
    
}

add_recipe_bt.addEventListener("click", add_recipe);




