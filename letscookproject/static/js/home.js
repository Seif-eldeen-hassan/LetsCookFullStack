let popular_card_arr = document.querySelectorAll(".popular_card");
const csrf_token = document.querySelector('#csrf_token')?.value;

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

for (let i = 0; i < popular_card_arr.length; i++) {
    let fav_bt = popular_card_arr[i].querySelector(".Favourite_recipe_home");
    fav_bt.addEventListener("click", function (e) {
        e.preventDefault();
        check_fav(e, ".popular_card");
    });
}

for(let i = 0; i < popular_card_arr.length; i++){
    let learn_bt = popular_card_arr[i].querySelector(".learn_more");
    learn_bt.addEventListener("click",function(e){ 
        e.preventDefault();  
        let current_recipe_id = e.target.closest(".popular_card").dataset.recipeId;
        window.location.href = `/recipes/${current_recipe_id}/ingredients`;
    })
}
