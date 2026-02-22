const apiURL = "http://127.0.0.1:5000/products";

const form = document.getElementById("productForm");

let editProductId = null;

form.addEventListener("submit", async function(e){

    e.preventDefault();

    const name = document.getElementById("name").value;
    const price = document.getElementById("price").value;
    const quantity = document.getElementById("quantity").value;

    const product = {
        name: name,
        price: price,
        quantity: quantity
    };

    if(editProductId){

        await fetch(`${apiURL}/${editProductId}`,{
            method:"PUT",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify(product)
        });

        editProductId = null;

    } else {

        await fetch(apiURL,{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify(product)
        });

    }

    loadProducts();
    form.reset();
});


async function loadProducts(){

    const response = await fetch(apiURL);
    const products = await response.json();

    const table = document.getElementById("productTable");

    table.innerHTML = "";

    products.forEach(product => {

        let stockStatus = "";

        if(product.quantity < 5){
            stockStatus = `<span class="low-stock">⚠ Low Stock</span>`;
        }

        const row = `
        <tr>
            <td>${product.id}</td>
            <td>${product.name}</td>
            <td>${product.price}</td>
            <td>${product.quantity}</td>
            <td>${stockStatus}</td>
            <td>
                <button class="edit" onclick="editProduct(${product.id}, '${product.name}', ${product.price}, ${product.quantity})">Edit</button>
                <button class="delete" onclick="deleteProduct(${product.id})">Delete</button>
            </td>
        </tr>
        `;

        table.innerHTML += row;

    });

}


async function deleteProduct(id){

    await fetch(`${apiURL}/${id}`,{
        method:"DELETE"
    });

    loadProducts();
}


function editProduct(id, name, price, quantity){

    document.getElementById("name").value = name;
    document.getElementById("price").value = price;
    document.getElementById("quantity").value = quantity;

    editProductId = id;

}


loadProducts();