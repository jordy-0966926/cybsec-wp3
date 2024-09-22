"use client";
import { useEffect, useState } from "react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

export function RecentResults() {
  const [students, setStudents] = useState([]);
  const [classes, setClasses] = useState([]);

  const fetchStudents = async () => {
    try {
      const response = await fetch(`/api/student`);
      const data = await response.json();
      setStudents(data);
    } catch (error) {
      console.error("Error fetching students:", error);
    }
  };

  const fetchClasses = async () => {
    try {
      const response = await fetch(`/api/class`);
      const data = await response.json();
      setClasses(data);
    } catch (error) {
      console.error("Error fetching classes:", error);
    }
  };

  //https://stackoverflow.com/questions/35206125/how-can-i-find-and-update-values-in-an-array-of-objects
  const getClass = (classId) => {
    const foundClass = classes.find((cls) => cls.id === classId);
    return foundClass ? foundClass.name : null;
  };

  useEffect(() => {
    fetchClasses();
  }, []);

  useEffect(() => {
    fetchStudents();
  }, []);

  return (
    <div className="space-y-8">
      {students.length === 0 ? (
        <p className="text-sm font-medium leading-none">Nog geen resultaten</p>
      ) : (
        <div className="space-y-8">
          {students.slice(0, 5).map((item) => (
            <div key={item.id} className="flex items-center">
              <Avatar className="h-9 w-9">
                <AvatarImage src="/avatars/05.png" alt="Avatar" />
                <AvatarFallback>{item.name[0]}</AvatarFallback>
              </Avatar>
              <div className="ml-4 space-y-1">
                <p className="text-sm font-medium leading-none">
                  {getClass(item.class)} | {item.name}
                </p>
                <p className="text-sm text-muted-foreground">
                  {item.student_num}@hr.nl
                </p>
              </div>
              <div className="ml-auto font-medium">
                Type: {item.type ?? "----"}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
