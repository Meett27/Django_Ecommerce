var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productID = this.dataset.product
        var action = this.dataset.action
        console.log('productid :', productID, 'action:', action)

        console.log('User', user)
        if (user === 'AnonymousUser') {
            console.log("User is Not Logged in")
        } else {
            updateUserOrder(productID, action)
        }

    })
}

function updateUserOrder(productID, action) {
    console.log("User is Logged in and Sending Data....")

    var url = '/update_cart_items/'

    fetch(url, {
        method: 'POST',
        headers: {
            'content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ 'productId': productID, 'action': action })
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            console.log('data:', data)
            location.reload()
        })
}