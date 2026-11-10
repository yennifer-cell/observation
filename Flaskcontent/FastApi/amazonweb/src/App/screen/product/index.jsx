
import useApp from "../../Hooks/useApp";

import useAxios from "../../Hooks/useAxios";

import { useEffect, useState } from "react";

function Screen() {
  const { member, token } = useApp();
  const request = useAxios();

  const [products, setProducts] = useState([]);

  const fetchProducts = async () => {
    let res = await request({
      method: "GET",
      url: "product",
    });

    if (res?._error) {
      return;
    }

    const responseData = res?.responseData;
    console.log(responseData);
    setProducts(responseData);
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleAddToCart = async (product) => {
    let res = await request({
      method: "POST",
      url: "client_order_product",
      data: {
        product_id: product.id,
        qty: 1,
      },
    });

    if (res?._error) {
      return;
    }

    const responseData = res?.responseData;
    console.log(responseData);
  };

  return (
    <div>
      <div>Hi {member?.name || "-"} </div>
      <div>Welcome to our site</div>

      {products.map((product) => {
        const img = product?.product_image[0]?.image || null;
        return (
          <div>
            <img src={img} />
            <div>{product?.name}</div>
            <div>{product?.description}</div>
            <button onClick={() => handleAddToCart(product)}>
              Add to cart
            </button>
          </div>
        );
      })}
    </div>
  );
}

export default Screen;
