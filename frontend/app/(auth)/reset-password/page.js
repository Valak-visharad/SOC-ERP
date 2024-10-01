"use client";
import { useState } from "react";
import { RiEyeLine, RiEyeOffLine } from "react-icons/ri";
import { LuLogIn } from "react-icons/lu";
import Image from "next/image";
import axiosPrivate from "@/axios/axiosPrivate";
import { useDispatch } from "react-redux";
import { addUser, setIsSessionLoaded, setLoggedin } from "@/store/features/common/userSlice";
import ResetPassword from "@/components/ResetPassword";
import { useRouter } from 'next/navigation'


export default function Page() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [isHidden, setIsHidden] = useState(true);
  const dispatch = useDispatch();
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };
  const router = useRouter();


  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const passwordRegex = /^(?=.[A-Za-z])(?=.\d)[A-Za-z\d]{8,}$/;

  function regexValidate() {
    if (!emailRegex.test(formData.username)) {
      alert("Please enter a valid email.");
      return false;
    }
    if (!passwordRegex.test(formData.password)) {
      alert(
        "Password must be at least 8 characters long and contain at least one letter and one number."
      );
      return false;
    }
    return true;
  }
  const handleSubmit =async() => {
    
    if (regexValidate) {
      try {
        
        const res = await axiosPrivate.post("/auth/login", formData);
        if (res.status == 200) {
          dispatch(setLoggedin(true));
          const userRes = await axiosPrivate.get("/auth/users/me");
          console.log(userRes);
          dispatch(addUser(userRes.data));
          const userRole = userRes.data.rolzzze;
          navigate(`/`);
        }
        console.log(res);
      } catch (error) {
        console.error("ERR::POST::LOGIN", error);
      }
    }
  };

  return (
    <div className="bg-white min-h-screen w-screen grid grid-cols-3">
      <div className="bg-black">
        <div
          style={{
            background: "url('/assets/img/uni.png')",
            backgroundSize: "cover",
            backgroundPosition: "right",
          }}
          className="h-screen md:block hidden "
        ></div>
      </div>
      <div className="flex justify-center items-center col-span-2 mit-bg-color">
        <div className="w-[50%] bg-white shadow-xl rounded-xl p-5 py-10 border border-gray-100">
          <Image
            src="/assets/img/mit-logo.png"
            width={140}
            height={80}
            className="mx-auto"
            alt="Picture of the author"
          />
                   <h1 className="text-center text-lg">Create New Password</h1>


          <ResetPassword/>

         
        </div>
      </div>
    </div>
  );
}
