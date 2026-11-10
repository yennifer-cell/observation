//for axios setup
import toast from "react-hot-toast";

import axios from "axios";

//custom hook.
//useState, useEffect → useAxios
//custom is a function that other hooks in react. render ui.
// logic.<> 

const base_url = "http://localhost:5000";

function useAxios() {
  const loadingId = "axios-loader";

  const request = async (requestObj) => {
    try {
      toast.loading("... Loading", { id: loadingId });

      const {
        method = "GET",
        url,
        data = {},
        headers = {},
      } = requestObj;

      let response = await axios({
        method,
        url: `${base_url}/${url}`,
        data,
      });

      const responseData = response?.data;
      return { response, responseData, _error: false };
    } catch (e) {
      const response = e?.response;
      const responseData = response?.data;
      const resDataMessage = responseData?.message;
      const resDataDetail = responseData?.detail;

      if (typeof resDataDetail === "string") {
        toast.error(resDataDetail);
      } else if (typeof resDataMessage === "string") {
        toast.error(resDataMessage);
      } else if (typeof e?.message === "string") {
        toast.error(e?.message);
      } else {
        toast.error("Request contact system admin");
      }

      return { response, responseData, _error: true };
    } finally {
      setTimeout(() => toast.dismiss(loadingId), 3000);
    }
  };

  return request;
}

export default useAxios;