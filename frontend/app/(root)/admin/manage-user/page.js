"use client";
import axiosPrivate from "@/axios/axiosPrivate";
import { useState, useEffect } from "react";
import { IoTrashBinSharp } from "react-icons/io5";
import { LuFileEdit } from "react-icons/lu";

const UserManagement = ({ tabName }) => {
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [faculty, setFaculty] = useState([]);
  const [student, setStudent] = useState([]);

  useEffect(() => {
    const fetchFaculty = async () => {
      try {
        const response = await axiosPrivate.get("/faculty/get");
        if (response.status === 200) {
          setFaculty(response.data);
        }
      } catch (error) {
        console.error("Error fetching faculty:", error);
      }
    };

    const fetchStudent = async () => {
      try {
        const response = await axiosPrivate.get("/students/get");
        if (response.status === 200) {
          setStudent(response.data);
        }
      } catch (error) {
        console.error("Error fetching students:", error);
      }
    };

    fetchFaculty();
    fetchStudent();
  }, []);

  const handleAddUser = () => {
    setIsPopupOpen(true);
  };

  const closePopup = () => {
    setIsPopupOpen(false);
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await axiosPrivate.post(
          "/auth/register/bulk",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        if (response.status === 200) {
          console.log("File uploaded successfully");
        } else {
          // Handle error
          console.error("File upload failed");
        }
      } catch (error) {
        console.error("Error uploading file:", error);
      }
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <input
          type="text"
          placeholder={`Search ${tabName}...`}
          className="border p-2 rounded-lg w-1/3"
        />
        <div className="flex space-x-4">
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
            onClick={handleAddUser}
          >
            Add {tabName}
          </button>
          <div className="flex items-center gap-2 bg-blue-500 hover:bg-blue-600 p-2 rounded-lg text-white">
            <label htmlFor={tabName} className="cursor-pointer">
              Upload file
            </label>
            <input
              type="file"
              id={tabName}
              accept=".xls,.xlsx"
              className="bg-gray-200 text-black px-4 py-2 rounded-lg hidden"
              onChange={handleFileUpload}
            />
          </div>
        </div>

        {isPopupOpen && (
          <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white p-4 rounded-lg w-[40vw]">
              <h2 className="text-lg mb-4 text-center">Add {tabName}</h2>
              <form className="grid grid-cols-3 gap-2">
                <input
                  type="text"
                  placeholder="Name"
                  className="border p-2 rounded"
                />
                <input
                  type="email"
                  placeholder="Email"
                  className="border p-2 rounded"
                />
                <input
                  type="text"
                  placeholder="Roll Number"
                  className="border p-2 rounded"
                />
                <input
                  type="text"
                  placeholder="Enrollment Number"
                  className="border p-2 rounded"
                />
                <input
                  type="text"
                  placeholder="Department"
                  className="border p-2 rounded"
                />
                <input
                  type="text"
                  placeholder="Year"
                  className="border p-2 rounded"
                />
                <input
                  type="text"
                  placeholder="Admission Year"
                  className="border p-2 rounded"
                />
                <input
                  type="text"
                  placeholder="Course Name"
                  className="border p-2 rounded"
                />
                <input
                  type="text"
                  placeholder="Specialization"
                  className="border p-2 rounded"
                />
                <input
                  type="text"
                  placeholder="Division"
                  className="border p-2 rounded"
                />
                <input
                  type="number"
                  placeholder="Age"
                  className="border p-2 rounded"
                />
                <input
                  type="text"
                  placeholder="Phone"
                  className="border p-2 rounded"
                />
                <input
                  type="text"
                  placeholder="Blood Group"
                  className="border p-2 rounded"
                />
                <input
                  type="text"
                  placeholder="Secondary Phone"
                  className="border p-2 rounded"
                />
                <input
                  type="text"
                  placeholder="Gender"
                  className="border p-2 rounded"
                />
                <input
                  type="date"
                  placeholder="Date of Birth"
                  className="border p-2 rounded"
                />
                <input
                  type="text"
                  placeholder="Guardian Type"
                  className="border p-2 rounded"
                />
                <input
                  type="text"
                  placeholder="Guardian Name"
                  className="border p-2 rounded"
                />
                <input
                  type="text"
                  placeholder="Guardian Phone"
                  className="border p-2 rounded"
                />
                <div className="flex justify-between col-span-3 mt-4">
                  <button
                    type="submit"
                    className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
                  >
                    Submit
                  </button>
                  <button
                    type="button"
                    onClick={closePopup}
                    className="text-red-500"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-300">
          <thead>
            <tr>
              {tabName === "Student" ? (
                <>
                  <th className="py-2 px-4 border">ID</th>
                  <th className="py-2 px-4 border">Name</th>
                  <th className="py-2 px-4 border">Email</th>
                  <th className="py-2 px-4 border">Roll Number</th>
                  <th className="py-2 px-4 border">Enrollment Number</th>
                  <th className="py-2 px-4 border">Department</th>
                  <th className="py-2 px-4 border">Year</th>
                  <th className="py-2 px-4 border">Admission Year</th>
                  <th className="py-2 px-4 border">Course Name</th>
                  <th className="py-2 px-4 border">Specialization</th>
                  <th className="py-2 px-4 border">Phone</th>
                  <th className="py-2 px-4 border">Age</th>
                  <th className="py-2 px-4 border">Actions</th>
                </>
              ) : (
                <>
                  <th className="py-2 px-4 border">ID</th>
                  <th className="py-2 px-4 border">Name</th>
                  <th className="py-2 px-4 border">Email</th>
                  <th className="py-2 px-4 border">Qualification</th>
                  <th className="py-2 px-4 border">Department</th>
                  <th className="py-2 px-4 border">Year</th>
                  <th className="py-2 px-4 border">Phone</th>
                  <th className="py-2 px-4 border">Age</th>
                  <th className="py-2 px-4 border">Actions</th>
                </>
              )}
            </tr>
          </thead>
          <tbody>
            {student.map((student, index) => (
              <tr key={index}>
                <td className="py-2 px-4 border">{student.id}</td>
                <td className="py-2 px-4 border">{student.name}</td>
                <td className="py-2 px-4 border">{student.email}</td>
                <td className="py-2 px-4 border">{student.rollNumber}</td>
                <td className="py-2 px-4 border">{student.enrollmentNumber}</td>
                <td className="py-2 px-4 border">{student.department}</td>
                <td className="py-2 px-4 border">{student.year}</td>
                <td className="py-2 px-4 border">{student.admissionYear}</td>
                <td className="py-2 px-4 border">{student.courseName}</td>
                <td className="py-2 px-4 border">{student.specialization}</td>
                <td className="py-2 px-4 border">{student.phone}</td>
                <td className="py-2 px-4 border">{student.age}</td>
                <td className="py-2 px-4 border">
                  <div className="flex justify-center items-center gap-4">
                    <div className="relative group">
                      <button className="text-yellow-500 text-2xl">
                        <LuFileEdit />
                      </button>
                      <span className="absolute left-1/2 transform -translate-x-1/2 -translate-y-full bg-gray-700 text-white text-xs rounded p-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                        Edit
                      </span>
                    </div>
                    <div className="relative group">
                      <button className="text-red-500 text-2xl">
                        <IoTrashBinSharp />
                      </button>
                      <span className="absolute left-1/2 transform -translate-x-1/2 -translate-y-full bg-gray-700 text-white text-xs rounded p-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                        Delete
                      </span>
                    </div>
                  </div>
                </td>
              </tr>
            ))}
            {tabName !== "Student" &&
              faculty.map((faculty, index) => (
                <tr key={index}>
                  <td className="py-2 px-4 border">{faculty.id}</td>
                  <td className="py-2 px-4 border">{faculty.name}</td>
                  <td className="py-2 px-4 border">{faculty.email}</td>
                  <td className="py-2 px-4 border">{faculty.qualification}</td>
                  <td className="py-2 px-4 border">{faculty.department}</td>
                  <td className="py-2 px-4 border">{faculty.year}</td>
                  <td className="py-2 px-4 border">{faculty.phone}</td>
                  <td className="py-2 px-4 border">{faculty.age}</td>
                  <td className="py-2 px-4 border">
                    <div className="flex justify-center items-center gap-4">
                      <div className="relative group">
                        <button className="text-yellow-500 text-2xl">
                          <LuFileEdit />
                        </button>
                        <span className="absolute left-1/2 transform -translate-x-1/2 -translate-y-full bg-gray-700 text-white text-xs rounded p-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                          Edit
                        </span>
                      </div>
                      <div className="relative group">
                        <button className="text-red-500 text-2xl">
                          <IoTrashBinSharp />
                        </button>
                        <span className="absolute left-1/2 transform -translate-x-1/2 -translate-y-full bg-gray-700 text-white text-xs rounded p-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                          Delete
                        </span>
                      </div>
                    </div>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

const Page = () => {
  const [activeTab, setActiveTab] = useState("tab1");

  const renderTabContent = () => {
    switch (activeTab) {
      case "tab1":
        return <UserManagement tabName="Faculty" />;
      case "tab2":
        return <UserManagement tabName="Student" />;
      case "tab3":
        return <UserManagement tabName="Alumni" />;
      default:
        return null;
    }
  };

  return (
    <div className="p-4">
      <div className="flex flex-row mb-4 gap-4">
        <button
          onClick={() => setActiveTab("tab1")}
          className={`py-2 px-4 rounded-t-lg ${
            activeTab === "tab1" ? "bg-blue-500 text-white" : "bg-gray-200"
          }`}
        >
          Faculty
        </button>
        <button
          onClick={() => setActiveTab("tab2")}
          className={`py-2 px-4 rounded-t-lg ${
            activeTab === "tab2" ? "bg-blue-500 text-white" : "bg-gray-200"
          }`}
        >
          Student
        </button>
        <button
          onClick={() => setActiveTab("tab3")}
          className={`py-2 px-4 rounded-t-lg ${
            activeTab === "tab3" ? "bg-blue-500 text-white" : "bg-gray-200"
          }`}
        >
          Alumni
        </button>
      </div>
      {renderTabContent()}
    </div>
  );
};

export default Page;
