let view_int_arr = document.querySelectorAll(".view_int")
let recipe_card_arr = document.querySelectorAll(".recipe_card");
const csrf_token = document.querySelector('#csrf_token')?.value;


for(let i = 0 ; i < view_int_arr.length ; i++){
    view_int_arr[i].addEventListener("click",function(e){ 
        e.preventDefault();  
        let current_recipe_id = e.target.closest(".recipe_card").dataset.recipeId;
        window.location.href = `/recipes/${current_recipe_id}/ingredients`;
    })
}

function delete_recipe(e) {
    const card = e.target.closest(".recipe_card");
    const recipe_id = card.dataset.recipeId;

    fetch("/ajax/delete-recipe/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        },
        body: JSON.stringify({ recipe_id: recipe_id })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            card.remove();  
        } else {
            alert("Failed to delete: " + data.error);
        }
    })
    .catch(error => {
        console.error("Deletion failed:", error);
    });
}


function edit_recipe(e) {
    e.preventDefault();
    const card = e.target.closest(".recipe_card");
    const recipe_id = card.dataset.recipeId;
    window.location.href = `/recipes/edit/${recipe_id}/`;
}



for (let i = 0; i < recipe_card_arr.length; i++) {
    let delete_bt = recipe_card_arr[i].querySelector(".delete_recipe");
    let edit_bt = recipe_card_arr[i].querySelector(".edit_icon");
    delete_bt.addEventListener("click", function (e) {delete_recipe(e);});
    edit_bt.addEventListener("click", function (e) {edit_recipe(e);});
}
