document.addEventListner("DOMContentLoaded", function() => {
	const productContainer = document.getElementById("product-container");
	async function getData() {
		let query = document.getElementById('inputtext4').value;
		let category = '';
		let filterBy = document.get // TO DO
		const response = await fetch(`search/${query}/${category}/${filterBy}/${minPrice}/${maxPrice}`, {
			method: 'POST',
			headers: {
			  'Content-Type': 'application/json',
			  // 'X-CSRFToken': getCSRFToken()
			},
			body: JSON.stringify({query: '',
								  category: '',
								  filterBy: '',
								  minPrice: '',
								  maxPrice: ''})
		});

	  const data = await response.json();
	  return data;
	}
	
	let items = getData();
	
	// Append items to container
	items.forEach(item => {
		productContainer.appendChild(createProductCard(item));
	});
	
	// Filter out Items
	const searchInput = document.getElementById("search");
    const categoryFilter = document.getElementById("category");
    const productContainer = document.getElementById("product-container");

    function filterProducts() {
        let searchQuery = searchInput.value.toLowerCase();
        let selectedCategory = categoryFilter.value;

        productContainer.innerHTML = ""; // Clear previous results

        items.forEach(item => {
            if (
                (item.title.toLowerCase().includes(searchQuery) || item.description.toLowerCase().includes(searchQuery)) &&
                (selectedCategory === "all" || item.category === selectedCategory)
            ) {
                productContainer.appendChild(createProductCard(item)); // Use your function to create cards
            }
        });
    }

    searchInput.addEventListener("input", filterProducts);
    categoryFilter.addEventListener("change", filterProducts);
})

function createProductCard(item) {
	const colDiv = document.createElement("div");
	colDiv.classList.add("col-lg-4", "col-md-6");

	const productItemDiv = document.createElement("div");
	productItemDiv.classList.add("product-item", "bg-light");

	const cardDiv = document.createElement("div");
	cardDiv.classList.add("card");

	const thumbContentDiv = document.createElement("div");
	thumbContentDiv.classList.add("thumb-content");

	const priceDiv = document.createElement("div");
	priceDiv.classList.add("price");
	priceDiv.textContent = item.price;

	const link = document.createElement("a");
	link.href = "single.html";

	const img = document.createElement("img");
	img.classList.add("card-img-top", "img-fluid");
	img.src = item.image;
	img.alt = item.title;

	link.appendChild(img);
	thumbContentDiv.appendChild(priceDiv);
	thumbContentDiv.appendChild(link);

	const cardBodyDiv = document.createElement("div");
	cardBodyDiv.classList.add("card-body");

	const title = document.createElement("h4");
	title.classList.add("card-title");

	const titleLink = document.createElement("a");
	titleLink.href = "#";
	titleLink.textContent = item.title;

	title.appendChild(titleLink);

	const productMetaUl = document.createElement("ul");
	productMetaUl.classList.add("list-inline", "product-meta");

	const categoryLi = document.createElement("li");
	categoryLi.classList.add("list-inline-item");

	const categoryLink = document.createElement("a");
	categoryLink.href = "single.html";
	categoryLink.innerHTML = `<i class="fa fa-folder-open-o"></i> ${item.category}`;

	categoryLi.appendChild(categoryLink);

	const stockLi = document.createElement("li");
	stockLi.classList.add("list-inline-item");

	const stockLink = document.createElement("a");
	stockLink.href = "#";
	stockLink.innerHTML = `<i class="fa fa-calendar"></i> ${item.stockStatus}`;

	stockLi.appendChild(stockLink);

	productMetaUl.appendChild(categoryLi);
	productMetaUl.appendChild(stockLi);

	const descriptionP = document.createElement("p");
	descriptionP.classList.add("card-text");
	descriptionP.textContent = item.description;

	const ratingsDiv = document.createElement("div");
	ratingsDiv.classList.add("product-ratings");

	const ratingsUl = document.createElement("ul");
	ratingsUl.classList.add("list-inline");

	for (let i = 0; i < 4; i++) {
		const starLi = document.createElement("li");
		starLi.classList.add("list-inline-item", "selected");
		starLi.innerHTML = '<i class="fa fa-star"></i>';
		ratingsUl.appendChild(starLi);
	}

	const unselectedStarLi = document.createElement("li");
	unselectedStarLi.classList.add("list-inline-item");
	unselectedStarLi.innerHTML = '<i class="fa fa-star"></i>';
	ratingsUl.appendChild(unselectedStarLi);

	ratingsDiv.appendChild(ratingsUl);

	// Append elements in proper hierarchy
	cardBodyDiv.appendChild(title);
	cardBodyDiv.appendChild(productMetaUl);
	cardBodyDiv.appendChild(descriptionP);
	cardBodyDiv.appendChild(ratingsDiv);

	cardDiv.appendChild(thumbContentDiv);
	cardDiv.appendChild(cardBodyDiv);

	productItemDiv.appendChild(cardDiv);
	colDiv.appendChild(productItemDiv);

	return colDiv;
}
