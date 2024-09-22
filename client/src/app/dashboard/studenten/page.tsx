"use client";
import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { MainNav } from "./components/main-nav";
import { UserNav } from "../components/user-nav";
import { DataTable } from "./components/table";

export default function DashboardPage() {
  const [students, setStudents] = useState([]);
  const [classes, setClasses] = useState([]);

  const fetchStudents = async () => {
    const response = await fetch(`/api/student`);
    const data = await response.json();
    setStudents(data);
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

  useEffect(() => {
    fetchStudents();
    fetchClasses();
  }, []);

  return (
    <>
      <div className="flex-col max-w-6xl m-auto md:flex">
        <div className="border-b">
          <div className="flex items-center h-16 px-4">
            <MainNav className="mx-6" />
            <div className="flex items-center ml-auto space-x-4">
              <UserNav />
            </div>
          </div>
        </div>
        <div className="flex-1 p-8 pt-6 space-y-4">
          <div className="flex items-center justify-between space-y-2">
            <h2 className="text-3xl font-bold tracking-tight">Klassen</h2>
            <div className="flex items-center space-x-2">
              <Button>Download</Button>
            </div>
          </div>
          <Tabs defaultValue="1A" className="space-y-4">
            <TabsList>
              {classes.map((cls) => (
                <TabsTrigger key={cls.id} value={cls.name}>
                  {cls.name}
                </TabsTrigger>
              ))}
            </TabsList>
            {classes.map((cls) => (
              <TabsContent key={cls.id} value={cls.name} className="space-y-4">
                <div className="grid gap-4 md:grid-cols-2 ">
                  <Card className="col-span-3">
                    <CardHeader>
                      <CardTitle>Studenten</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <DataTable
                        data={students.filter(
                          (student) => student.class === cls.id
                        )}
                      />
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>
            ))}
          </Tabs>
        </div>
      </div>
    </>
  );
}
