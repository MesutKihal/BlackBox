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
		let page = [];
		if (sortBy.value == "1")
		{
			products.sort((a, b) => b.rating - a.rating);
		} else if (sortBy.value == "2")
		{
			products.sort((a, b) => a.price - b.price);
		} else if (sortBy.value == "3") 
		{
			products.sort((a, b) => b.price - a.price);
		}
		
		// Filter without search
		if (input.value == "")
		{
			document.getElementById('searchQuery').innerText = "";
			document.getElementById('resultCount').innerText = "";
			list.innerHTML = '';
			// products.length = 0;
			// products.push(...originalProducts);
			page = paginate(filteredProducts(products));
			if (page)
			{
				page.forEach((product, i) => {
					let card = createProductCard(product);
					if (viewSwitcher.dataset.view == "grid")
					{
						card = createProductCard(product);
					} else {
						card = createProductStrip(product);
					}
					
					card.animate([
						{transform: "translateY(-50px)"},
						{transform: "translateY(0px)"}
					], {
						duration: 500+(i*100),
						easing: "ease",
					})
					list.appendChild(card);
				})
			}
		} // Search & Filter
		else {
			let searchResult = fuse.search(input.value);
			list.innerHTML = '';
			
			document.getElementById('searchQuery').innerText = `Results For "${input.value}",`;
			document.getElementById('resultCount').innerText = `${searchResult.length} Results`;
			
			searchResult.map(result => {
				page.push(result.item)
			});
			page = paginate(filteredProducts(page));
			if (page)
			{
				page.forEach((product, i) => {
					let card = createProductCard(product)
					if (viewSwitcher.dataset.view == "grid")
					{
						card = createProductCard(product);
					} else {
						card = createProductStrip(product);
					}
					card.animate([
							{transform: "translateY(-50px)"},
							{transform: "translateY(0px)"}
						], {
							duration: 500+(i*300),
							easing: "ease",
					})
					list.appendChild(card);
				})
			}
			//.join('');
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
	function filteredProducts(products) {
		let categories = categoryFilter();
		let values = priceFilter.value.split(',');
		let isAvailable = document.getElementById('filter2');
		const min = Number(values[0]);
		const max = Number(values[1]);

		return products.filter(product => {
			const priceMatch = product.price >= min && product.price <= max;
			const stockMatch = isAvailable.value === "both" || isAvailable.value == product.inStock;
			const categoryMatch = categories.length === 0 || categories.includes(product.category);

			return priceMatch && stockMatch && categoryMatch;
		});
	}
	// Listen to the search input and category filter
	let input = document.getElementById('inputtext4');
	let list = document.querySelector('#product-container');
	let categoryFilters = document.getElementsByName('categoryFilter');
	let categorySelect = document.getElementById("categorySelect");
	let subCategories = document.getElementById("subCategories");
	let priceFilter = document.getElementById("Price");
	let viewSwitcher = document.getElementById("viewSwitcher");
	let listView = document.getElementById('listView');
	let gridView = document.getElementById('gridView');
	let previousPage = document.getElementById('previousPage');
	let nextPage = document.getElementById('nextPage');
	let paginationControl = document.getElementById("pagination");
	let sortBy = document.getElementById('filter1');
	let isAvailable = document.getElementById('filter2');
	
	let products = [];
	let fuse = new Fuse()
	let originalProducts = []
	let categories = []
	
	
	// Intializing the category filter
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
	
	// Initializing the fuse search
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
		
		gridView.onclick = (event) => {
			if (viewSwitcher.dataset.view == 'list') {
				switchView();
				updateProducts();
			}
		}
		listView.onclick = (event) => {
			if (viewSwitcher.dataset.view == 'grid') {
				switchView();
				updateProducts();
			}
		}
		
		previousPage.onclick = (event) => {
			paginationControl.dataset.pageNumber = Number(paginationControl.dataset.pageNumber) - 1;
			updateProducts();
		}
		
		nextPage.onclick = (event) => {
			paginationControl.dataset.pageNumber = Number(paginationControl.dataset.pageNumber) + 1;
			updateProducts();	
		}
		
		sortBy.onchange = (event) => {
			paginationControl.dataset.pageNumber = 1;
			updateProducts();
		}
		
		isAvailable.onchange = (event) => {
			updateProducts();
		}
	})	
})

// Create product card
function createProductCard(item) {
    const colDiv = document.createElement("div");
    colDiv.classList.add("col-lg-4", "col-md-4", "mb-4");

    const cardDiv = document.createElement("div");
    cardDiv.classList.add("card", "h-100", "border-0", "shadow", "product-card", "overflow-hidden");

    // Product image
    const imgLink = document.createElement("a");
    imgLink.href = "#";

    const img = document.createElement("img");
    img.classList.add("card-img-top", "img-fluid", "p-3", "product-image");
    img.src = item.image;
    img.alt = item.title;

    imgLink.appendChild(img);
    cardDiv.appendChild(imgLink);

    // Card Body
    const cardBodyDiv = document.createElement("div");
    cardBodyDiv.classList.add("card-body", "p-2", "text-center");

    // Price
    const priceDiv = document.createElement("h5");
    priceDiv.classList.add("fw-bold", "text-success", "mb-2");
    priceDiv.textContent = item.price;

    // Title
    const title = document.createElement("h6");
    title.classList.add("card-title", "mb-1", "text-truncate"); 
    title.textContent = item.title;

    // Category
    const category = document.createElement("small");
    category.classList.add("text-muted", "d-block", "mb-2", "text-truncate");
    category.textContent = item.category;

    // Stock Status
    const stockStatusDiv = document.createElement("span");
	if (item.inStock == "1")
	{
		stockStatusDiv.classList.add("badge", "bg-success", "text-white", "mb-2", "mr-2", "fs-6", "p-2");
		stockStatusDiv.textContent = "In Stock";
	} else {
		stockStatusDiv.classList.add("badge", "bg-danger", "text-white", "mb-2", "mr-2", "fs-6", "p-2");
		stockStatusDiv.textContent = "Out of Stock";
	}

    // Badges - Best Seller
    const bestSellerBadge = document.createElement("span");
    bestSellerBadge.classList.add("badge", "bg-primary", "text-white", "fs-6", "p-2", "mb-2");
    bestSellerBadge.textContent = "Best Seller"; // You can update this as needed later

    // Ratings - 5 stars by default
    const ratingsDiv = document.createElement("div");
    ratingsDiv.classList.add("product-ratings", "mb-2");

    const ratingsUl = document.createElement("ul");
    ratingsUl.classList.add("list-inline");

    // Create stars (Font Awesome)
    for (let i = 0; i < item.rating; i++) {
        const starLi = document.createElement("li");
        starLi.classList.add("list-inline-item", "selected");
        starLi.innerHTML = '<i class="fa fa-star"></i>';
        ratingsUl.appendChild(starLi);
    }

    ratingsDiv.appendChild(ratingsUl);

    // Button
    const btn = document.createElement("a");
    btn.href = "/single";
    btn.classList.add("btn", "btn-sm", "btn-outline-primary", "w-100");
    btn.textContent = "View Product";

    // Append everything
    cardBodyDiv.append(priceDiv, title, category, stockStatusDiv, bestSellerBadge, ratingsDiv, btn);

    cardDiv.appendChild(cardBodyDiv);
    colDiv.appendChild(cardDiv);

    return colDiv;
}

// Create Product Strip
function createProductStrip(item) {
    const rowDiv = document.createElement("div");
    rowDiv.classList.add("row", "mb-4", "product-list-item", "shadow", "ml-4");

    // Left side: Product Image
    const colImgDiv = document.createElement("div");
    colImgDiv.classList.add("col-4", "col-md-3", "p-3");

    const imgLink = document.createElement("a");
    imgLink.href = "#";

    const img = document.createElement("img");
    img.classList.add("img-fluid", "product-image", "list-view-img"); // Add custom class for list view
    img.src = item.image;
    img.alt = item.title;

    imgLink.appendChild(img);
    colImgDiv.appendChild(imgLink);

    // Right side: Product Details
    const colDetailsDiv = document.createElement("div");
    colDetailsDiv.classList.add("col-8", "col-md-9", "p-3", "d-flex", "flex-column", "justify-content-between");

    // Card Body
    const cardBodyDiv = document.createElement("div");
    cardBodyDiv.classList.add("product-card-body", "d-flex", "flex-column", "h-100"); // Allow expansion to full height

    // Price
    const priceDiv = document.createElement("h5");
    priceDiv.classList.add("fw-bold", "text-success", "mb-2");
    priceDiv.textContent = item.price;

    // Title
    const title = document.createElement("h6");
    title.classList.add("card-title", "mb-1");
    title.textContent = item.title;

    // Category
    const category = document.createElement("small");
    category.classList.add("text-muted", "d-block", "mb-2");
    category.textContent = item.category;

    // Badges (Best Seller and In Stock)
    const badgesDiv = document.createElement("div");
    badgesDiv.classList.add("d-flex", "mb-2"); // Flex container to align badges side by side

    // Stock Status Badge
    const stockStatusDiv = document.createElement("span");
	if (item.inStock == "1")
	{
		stockStatusDiv.classList.add("badge", "bg-success", "text-white", "fs-6", "p-1", "mr-2");
		stockStatusDiv.textContent = "In Stock";
	} else {
		stockStatusDiv.classList.add("badge", "bg-danger", "text-white", "fs-6", "p-1", "mr-2");
		stockStatusDiv.textContent = "Out of Stock";
	}

    // Best Seller Badge
    const bestSellerBadge = document.createElement("span");
    bestSellerBadge.classList.add("badge", "bg-primary", "text-white", "fs-6", "p-1");
    bestSellerBadge.textContent = "Best Seller"; // You can update this as needed later

    // Add badges to badges container
    badgesDiv.appendChild(stockStatusDiv);
    badgesDiv.appendChild(bestSellerBadge);

    // Ratings - 5 stars by default
    const ratingsDiv = document.createElement("div");
    ratingsDiv.classList.add("product-ratings", "mb-2");

    const ratingsUl = document.createElement("ul");
    ratingsUl.classList.add("list-inline");

    // Create stars (Font Awesome)
    for (let i = 0; i < item.rating; i++) {
        const starLi = document.createElement("li");
        starLi.classList.add("list-inline-item", "selected");
        starLi.innerHTML = '<i class="fa fa-star"></i>';
        ratingsUl.appendChild(starLi);
    }

    ratingsDiv.appendChild(ratingsUl);

    // Button
    const btn = document.createElement("a");
    btn.href = "#";
    btn.classList.add("btn", "btn-sm", "btn-outline-primary", "mt-2", "w-50");
    btn.textContent = "View Product";

    // Append everything
    cardBodyDiv.append(title, priceDiv, category, badgesDiv, ratingsDiv, btn);

    // Append card body to details div
    colDetailsDiv.appendChild(cardBodyDiv);

    // Append columns to row
    rowDiv.appendChild(colImgDiv);
    rowDiv.appendChild(colDetailsDiv);

    return rowDiv;
}

// Create a category checkbox
function createCategoryCheckbox(categories) {
	const containerDiv = document.createElement('div');
	containerDiv.classList.add('d-flex', 'align-items-start', 'flex-column');
	let i = 0;
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
	  formCheckDiv.animate([
			{ transform: 'translateX(-50px)' },
			{ transform: 'translateX(0)' }
		  ], {
			duration: (500*i) + 500,
			easing: 'ease',
		});
	  containerDiv.appendChild(formCheckDiv);
	  i++
	});
	
	return containerDiv;
}

// Switch view 
function switchView()
{
	if (viewSwitcher.dataset.view == 'grid') 
	{
		viewSwitcher.dataset.view = "list";
		gridView.setAttribute('class', 'text-secondary');
		listView.setAttribute('class', 'text-primary');
	} else {
		viewSwitcher.dataset.view = "grid";
		gridView.setAttribute('class', 'text-primary');
		listView.setAttribute('class', 'text-secondary');
	}
}

function paginate(products) 
{
	let itemsPerPage = 6;
	let pageCount = Math.ceil(products.length / itemsPerPage);
	let paginationControl = document.getElementById("pagination");
	let currentPage = document.getElementById("CurrentPage");
	let pages = [];
	paginationControl.dataset.pageCount = pageCount;
	for (let i = 0; i < products.length; i += itemsPerPage)
	{
		pages.push(products.slice(i, i + itemsPerPage))
	}
	if (paginationControl.dataset.pageNumber > pageCount)
	{
		paginationControl.dataset.pageNumber = pageCount;
	} else if (paginationControl.dataset.pageNumber <= 0) {
		paginationControl.dataset.pageNumber = 1;
	}
	currentPage.innerText = paginationControl.dataset.pageNumber;
	return pages[paginationControl.dataset.pageNumber - 1];
}
