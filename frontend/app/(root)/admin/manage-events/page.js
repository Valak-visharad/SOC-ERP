"use client";
import { format } from "path";
import { useSelector } from "react-redux";
import { useEffect, useState, useCallback } from "react";
import { IoPencil } from "react-icons/io5";
import axiosPrivate from "@/axios/axiosPrivate";
import toast from "react-hot-toast";

const predefinedEvents = [];
const Page = () => {
  const user = useSelector((state) => state.user.user);
  const [currentEvents, setCurrentEvents] = useState(predefinedEvents); // Default to predefined events

  useEffect(() => {
    console.log("hey", user);
  }, [user]);

  const [newEventTitle, setNewEventTitle] = useState("");
  const [selectedDate, setSelectedDate] = useState(
    new Date().toLocaleDateString("en-CA").replace(/\//g, "-")
  );
  const [showPopup, setShowPopup] = useState(false);
  const [popupEvents, setPopupEvents] = useState([]);
  const [currentMonth, setCurrentMonth] = useState(new Date().getMonth());
  const [currentYear, setCurrentYear] = useState(new Date().getFullYear());
  const [editEventId, setEditEventId] = useState(null);
  const [editEventTitle, setEditEventTitle] = useState("");
  const [showAddEventPopup, setShowAddEventPopup] = useState(false);

  const handleNextMonth = () => {
    if (currentMonth === 11) {
      setCurrentMonth(0);
      setCurrentYear(currentYear + 1);
    } else {
      setCurrentMonth(currentMonth + 1);
    }
  };

  const handlePrevMonth = () => {
    if (currentMonth === 0) {
      setCurrentMonth(11);
      setCurrentYear(currentYear - 1);
    } else {
      setCurrentMonth(currentMonth - 1);
    }
  };

  const renderCalendar = () => {
    const days = daysInMonth(currentMonth, currentYear);
    const firstDay = new Date(currentYear, currentMonth, 1).getDay();

    const calendar = [];
    for (let i = 0; i < firstDay; i++) {
      calendar.push(<div key={`empty-${i}`} className="border p-4"></div>);
    }
    for (let day = 1; day <= days; day++) {
      const dateString = new Date(currentYear, currentMonth, day)
        .toLocaleDateString("en-CA")
        .replace(/\//g, "-");
      const isToday =
        dateString ===
        new Date().toLocaleDateString("en-CA").replace(/\//g, "-");
      const dayEvents = currentEvents.filter(
        (event) => event.date === dateString
      );
      calendar.push(
        <div
          key={day}
          className={`border p-4 relative flex flex-col h-44 ${
            isToday ? "bg-yellow-200 bg-opacity-35" : ""
          }`}
          onClick={() => {
            setSelectedDate(dateString);
            setShowAddEventPopup(true);
          }} // Open add event popup on date click
        >
          <span className="font-bold">{day}</span>
          <div className="flex-1">
            {dayEvents.map((event, index) => (
              // Check if the event is predefined
              <div
                key={event.id}
                className="bg-blue-200 p-1 rounded mt-1 z-9"
                onClick={(e) => e.stopPropagation()}
              >
                {event.title}
                <button
                  onClick={() => openEditModal(event)} // Open edit modal
                  className="text-yellow-500 ml-2"
                >
                  <IoPencil />
                </button>
                <button
                  onClick={() => handleDeleteEvent(event.id)}
                  className="text-red-500 ml-2"
                >
                  X
                </button>
              </div>
            ))}
            {dayEvents.length > 3 && (
              <button
                onClick={() => {
                  setPopupEvents(dayEvents);
                  setShowPopup(true);
                }}
                className="text-blue-500 mt-1"
              >
                +{dayEvents.length - 3} more
              </button>
            )}
          </div>
        </div>
      );
    }
    return calendar;
  };

  function handleAddEvent() {
    if (newEventTitle) {
      const newEvent = {
        event: newEventTitle,
        date: selectedDate,
      };
      axiosPrivate
        .post("/calender/add-event", newEvent)
        .then((response) => {
          setCurrentEvents([...currentEvents, response.data]);
          setNewEventTitle(newEventTitle);
          setShowAddEventPopup(false);
          toast.success("Event added successfully!"); // Toast for success
        })
        .catch((error) => {
          console.error("Error adding event:", error);
          toast.error("Failed to add event."); // Toast for error
        });
    }
  }

  function handleDeleteEvent(id) {
    axiosPrivate
      .delete(`/calender/delete-event/${id}`)
      .then(() => {
        setCurrentEvents(currentEvents.filter((event) => event.id !== id));
        toast.success("Event deleted successfully!"); // Toast for success
      })
      .catch((error) => {
        console.error("Error deleting event:", error);
        toast.error("Failed to delete event."); // Toast for error
      });
  }

  const openEditModal = (event) => {
    setEditEventId(event.id);
    setEditEventTitle(event.title);
  };

  const handleUpdateEvent = () => {
    if (editEventId && editEventTitle) {
      const updatedEvent = {
        id: editEventId, // Include the event ID
        event: editEventTitle, // Use the updated title
      };
      axiosPrivate
        .patch("/calender/update-event", updatedEvent) // Send updatedEvent directly
        .then(() => {
          const updatedEvents = currentEvents.map((event) =>
            event.id === editEventId
              ? { ...event, title: editEventTitle }
              : event
          );
          setCurrentEvents(updatedEvents);
          setEditEventId(null);
          setEditEventTitle("");
          toast.success("Event updated successfully!"); // Toast for success
        })
        .catch((error) => {
          console.error("Error updating event:", error); // Handle any errors
          toast.error("Failed to update event."); // Toast for error
        });
    }
  };

  const daysInMonth = (month, year) => {
    return new Date(year, month + 1, 0).getDate();
  };

  const currentUser = useSelector((state) => state.user.user);
  useEffect(() => {}, [user]);
  const [loading, setLoading] = useState(false); // Add loading state

  const fetchAllEvents = useCallback(async () => {
    try {
      const response = await axiosPrivate.get(
        `/calender/fetch-events?current_user_id=${user.id}`
      );
      console.log("Fetch response:", response); // Log the response object
      const data = response.data; // Use response.data directly
      console.log("Fetched data:", data); // Log the fetched data

      // Map the fetched data to match the expected format
      const formattedEvents = data.map((event) => ({
        id: event.id, // Ensure you have an id field
        title: event.event, // Use event.event for the title
        date: event.date, // Ensure you have a date field
      }));

      setCurrentEvents(formattedEvents); // Set current events with formatted data
    } catch (error) {
      console.error("Failed to fetch events:", error);
      toast.error("Failed to fetch events."); // Show error toast
    }
  }, [user]);

  useEffect(() => {
    if (user && user.id) {
      // Check if user is not null and has an id
      fetchAllEvents(); // Call the function to fetch events
    }
  }, [fetchAllEvents, user]); // Add user.id as a dependency

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Event Calendar</h1>
      <div className="flex justify-between mt-6">
        <button onClick={handlePrevMonth} className="bg-gray-300 p-2 rounded">
          Previous
        </button>
        <h2 className="text-xl">{`${new Date(
          currentYear,
          currentMonth
        ).toLocaleString("default", { month: "long" })} ${currentYear}`}</h2>
        <button onClick={handleNextMonth} className="bg-gray-300 p-2 rounded">
          Next
        </button>
      </div>
      <div className="grid grid-cols-7 gap-4 mt-4">
        {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((day) => (
          <div key={day} className="font-bold text-center">
            {day}
          </div>
        ))}
        {renderCalendar()}
      </div>

      {showPopup && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
          <div className="bg-white p-4 rounded shadow-lg">
            <h2 className="text-xl font-bold mb-2">Events</h2>
            <ul>
              {popupEvents.map((event) => (
                <li key={event.id} className="flex justify-between">
                  <span>
                    {event.title} - {event.date}
                  </span>
                  <button
                    onClick={() => handleDeleteEvent(event.id)}
                    className="text-red-500"
                  >
                    X
                  </button>
                </li>
              ))}
            </ul>
            <button
              onClick={() => setShowPopup(false)}
              className="mt-4 bg-blue-500 text-white p-2 rounded"
            >
              Close
            </button>
          </div>
        </div>
      )}

      {editEventId && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
          <div className="bg-white p-4 rounded shadow-lg">
            <h2 className="text-xl font-bold mb-2">Edit Event</h2>
            <input
              type="text"
              value={editEventTitle}
              onChange={(e) => setEditEventTitle(e.target.value)}
              className="border p-2 mb-4 w-full"
            />
            <button
              onClick={handleUpdateEvent}
              className="bg-blue-500 text-white p-2 rounded w-full"
            >
              Update Event
            </button>
            <button
              onClick={() => setEditEventId(null)}
              className="mt-2 bg-gray-300 text-black p-2 rounded w-full"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {showAddEventPopup && ( // Add event popup
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
          <div className="bg-white p-4 rounded shadow-lg">
            <h2 className="text-xl font-bold mb-2">Add Event</h2>
            <input
              type="text"
              value={newEventTitle}
              onChange={(e) => setNewEventTitle(e.target.value)}
              placeholder="Enter event title"
              className="border p-2 mb-4 w-full"
            />
            <button
              onClick={handleAddEvent}
              className="bg-blue-500 text-white p-2 rounded w-full"
            >
              Add Event
            </button>
            <button
              onClick={() => setShowAddEventPopup(false)}
              className="mt-2 bg-gray-300 text-black p-2 rounded w-full"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Page;
