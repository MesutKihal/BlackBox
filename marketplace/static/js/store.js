document.addEventListener("DOMContentLoaded", (event) => {
	// Get products from database
	async function getProducts() {
		try {
			const response = await fetch("get_products");
			if (!response.ok) {
				throw new Error(`Response status: ${response.status}`);
			}
			return response.json();
		} catch (error) {
			console.error(error.message);
			return;
		}
	}
	// Get categories from database
	async function getCategories() {
		try {
			const response = await fetch("get_categories");
			if (!response.ok) {
				throw new Error(`Response status: ${response.status}`)
			}
			return response.json();
		} catch (error) {
			console.error(error.message);
			return;
		}
	}
	// Check for checked checkboxes ""A lot of checks hhh""
	function categoryFilter() {
		let filters = document.getElementsByName('categoryFilter');
		let isChecked = []
		filters.forEach(filter => {
			if (filter.checked == true)
			{
				isChecked.push(filter.id);
			}
		})
		return isChecked;
	}
	// Update the products view
	function updateProducts() {
		let categories = categoryFilter();
		let values = priceFilter.value.split(',');
		// Filter without search
		if (input.value == "")
		{
			list.innerHTML = '';
			// products.length = 0;
			// products.push(...originalProducts);
			products.forEach(product => {
				if (categories.length == 0) {
					if (Number(values[0]) <= product.price && product.price <= Number(values[1]))
					{
						list.appendChild(createProductCard(product));
					}
				} else {
					for (var i = 0; i < categories.length; i++)
					{
						if (product.category == categories[i] && Number(values[0]) <= product.price && product.price <= Number(values[1]))
						{
							list.appendChild(createProductCard(product));
							break;
						}
					} 
				}
			})
		} // Search & Filter
		else {
			let searchResult = fuse.search(input.value);
			list.innerHTML = '';
			let html = searchResult.map(result => {
				const card = createProductCard(result.item)
				if (categories.length == 0) {
					if (Number(values[0]) <= result.item.price && result.item.price <= Number(values[1]))
					{
						list.appendChild(card);
					}
				} else {
					for (var i = 0; i < categories.length; i++)
					{
						if (result.item.category == categories[i] && Number(values[0]) <= result.item.price && result.item.price <= Number(values[1]))
						{
							list.appendChild(card);
							break;
						}
					} 
				}
				
			}).join('');
		}
	}
	// Update Checkboxes
	function updateCheckBoxes() {
		if (categorySelect.value == "0")
		{
			return;
		} else {
			subCategories.style.display = "block";
			subCategories.innerText = "";
			categories.forEach(category => {
				if (category.title == categorySelect.value)
				{
					subCategories.appendChild(createCategoryCheckbox(category.subcategories));
				}
			})
		}
	}
	// Listen to the search input and category filter
	let input = document.getElementById('inputtext4');
	let list = document.querySelector('#product-container');
	let categoryFilters = document.getElementsByName('categoryFilter');
	let categorySelect = document.getElementById("categorySelect");
	let subCategories = document.getElementById("subCategories");
	let priceFilter = document.getElementById("Price");
	let products = [];
	let fuse = new Fuse()
	let originalProducts = []
	let categories = []
	
	getCategories().then(data => {
		categories = data["categories"];
		categorySelect.onchange = (event) => {
			updateCheckBoxes();
			categoryFilters = document.getElementsByName('categoryFilter');
			categoryFilters.forEach(filter => {
				filter.onchange = (event) => {
					updateProducts();
				}			
			})
		}
	})
	getProducts().then(data => {
		products = data['items'];
		updateProducts();
		originalProducts = [...products];
		fuse = new Fuse(products, {
			keys: ['title'],
			threshold: 0.1
		});	
		
		input.addEventListener('input', () => {
			updateProducts();
		});
		
		priceFilter.onchange = (event) => {
			updateProducts();
		}
		
	})	
})

// Create product card 
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
	link.href = "";

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

// Create a category checkbox
function createCategoryCheckbox(categories) {
	const containerDiv = document.createElement('div');
	containerDiv.classList.add('d-flex', 'align-items-start', 'flex-column');

	categories.forEach(category => {
	  const formCheckDiv = document.createElement('div');
	  formCheckDiv.classList.add('form-check');

	  const checkboxInput = document.createElement('input');
	  checkboxInput.classList.add('form-check-input');
	  checkboxInput.type = 'checkbox';
	  checkboxInput.name = 'categoryFilter';
	  checkboxInput.id = category.id;

	  const label = document.createElement('label');
	  label.classList.add('form-check-label', 'text-dark');
	  label.setAttribute('for', category.id);
	  label.textContent = category.label;

	  formCheckDiv.appendChild(checkboxInput);
	  formCheckDiv.appendChild(label);

	  containerDiv.appendChild(formCheckDiv);
	});
	
	return containerDiv;
}