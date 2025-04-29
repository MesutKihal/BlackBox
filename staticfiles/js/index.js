
function categoryBlock(CategoryImage, Category, SubCategories) {
    // Create elements
    const colDiv = document.createElement('div');
    colDiv.className = 'col-lg-3 offset-lg-0 col-md-5 offset-md-1 col-sm-6';

    const categoryBlock = document.createElement('div');
    categoryBlock.className = 'category-block';

    const header = document.createElement('div');
    header.className = 'header';

    const categoryImg = document.createElement('img');
    categoryImg.className = 'icon-bg-1';
    categoryImg.src = `{% url '${CategoryImage}' %}`;

    const categoryTitle = document.createElement('h4');
    categoryTitle.textContent = Category;

    const categoryList = document.createElement('ul');
    categoryList.className = 'category-list';

    // Add subcategories dynamically
    SubCategories.forEach(sub => {
        const listItem = document.createElement('li');
        const link = document.createElement('a');
        link.href = '';

        const subTitle = document.createTextNode(sub.title);
        const countSpan = document.createElement('span');
        countSpan.textContent = sub.count;

        link.appendChild(subTitle);
        link.appendChild(countSpan);
        listItem.appendChild(link);
        categoryList.appendChild(listItem);
    });

    // Append elements
    header.appendChild(categoryImg);
    header.appendChild(categoryTitle);
    categoryBlock.appendChild(header);
    categoryBlock.appendChild(categoryList);
    colDiv.appendChild(categoryBlock);

    // Append to the DOM
    return colDiv
}

