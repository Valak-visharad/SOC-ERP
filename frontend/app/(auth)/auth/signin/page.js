"use client";
import { useState } from "react";
import { RiEyeLine, RiEyeOffLine } from "react-icons/ri";
import { LuLogIn } from "react-icons/lu";
import Image from "next/image";
import axiosPrivate from "@/axios/axiosPrivate";
import { useDispatch } from "react-redux";
import {
  addUser,
  setIsSessionLoaded,
  setLoggedin,
} from "@/store/features/common/userSlice";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";

export default function Page() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [isHidden, setIsHidden] = useState(true);
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();
  const router = useRouter();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

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
  const handleSubmit = async () => {
    if (regexValidate) {
      try {
        setLoading(true)
        const res = await axiosPrivate.post("/auth/login", formData);
        if (res.status == 200) {
          toast.success("Signin Successful");
          dispatch(setLoggedin(true));
          const userRes = await axiosPrivate.get("/auth/users/me");
          console.log(userRes);
          dispatch(addUser(userRes.data));
          router.push("/");
        }
        console.log(res);
      } catch (error) {
        console.error("ERR::POST::LOGIN", error);
        toast.error("Something went wrong")
      } finally{
        setLoading(false);
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
          <h1 className="text-center text-lg">MIT ADT University</h1>
          <p className="text-sm text-gray-500 text-center">SOC Portal</p>
          <div className="flex flex-col gap-y-6 px-10 my-8 mt-10">
            <div className="flex flex-col">
              <label htmlFor="email" className="text-base">
                Email
              </label>
              <input
                className="border p-2 rounded-md bg-gray-100"
                placeholder="Enter Email"
                type="text"
                value={formData.email}
                onChange={handleChange}
                name="email"
                id="email"
              />
            </div>
            <div className="flex flex-col">
              <label htmlFor="password" className="text-base">
                Password
              </label>
              <div className="relative">
                <input
                  className="border w-full p-2 rounded-md bg-gray-100"
                  placeholder="Enter Password"
                  value={formData.password}
                  onChange={handleChange}
                  type={isHidden ? "password" : "text"}
                  name="password"
                  id="password"
                />
                {isHidden ? (
                  <RiEyeOffLine
                    onClick={() => setIsHidden((prev) => !prev)}
                    className="absolute top-3 right-2 text-lg cursor-pointer"
                  />
                ) : (
                  <RiEyeLine
                    onClick={() => setIsHidden((prev) => !prev)}
                    className="absolute top-3 right-2 text-lg cursor-pointer"
                  />
                )}
              </div>
            </div>
          </div>

          <button
            onClick={handleSubmit}
            className=" bg-green-400 px-4 py-2 w-[7rem] h-[2.5rem] justify-center rounded-md text-white flex items-center gap-x-1 mx-auto mt-5 hover:bg-green-500 transition"
          >
            {loading ? <div className="w-4 h-4 rounded-full border-2 border-r-transparent animate-spin mx-auto"></div> :
              <>
                Sign in <LuLogIn />
              </>
            }{" "}
          </button>
        </div>
      </div>
    </div>
  );
}
