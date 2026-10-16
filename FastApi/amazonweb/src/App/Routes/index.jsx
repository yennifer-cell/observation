import { BrowserRouter, Routes, Route } from "react-router";


import LoginPage from "../screen/login";

import Signup from "../screen/signup";

import Product from "../screen/product";

import Order from "../screen/order";

function AppRoutes(){

    return (
        <BrowserRouter>
        <Routes>
        <Route path="/" element={<LoginPage/>}></Route>
        <Route path="/Signup" element={<Signup/>} ></Route>
        <Route path="/product" element={<Product />} />
        <Route path="/order" element={<Order />} />
        </Routes>


        </BrowserRouter>
    );
}
 export default AppRoutes;
   
