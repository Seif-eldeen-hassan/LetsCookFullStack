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

function check_fav(e, type) {
    let card = e.target.closest(type);
    let recipe_id = card.dataset.recipeId;

    fetch("/ajax/toggle-fav/", {
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
            const img = e.target;
            img.src = data.favorited ? "/static/images/favourite(2).png" : "/static/images/favourite.png";
        } else {
            alert("Error: " + data.error);
        }
    });
}

for (let i = 0; i < recipe_card_arr.length; i++) {
    let fav_bt = recipe_card_arr[i].querySelector(".Favourite_recipe");
    fav_bt.addEventListener("click", function (e) {
        e.preventDefault();
        check_fav(e, ".recipe_card");
    });
}
