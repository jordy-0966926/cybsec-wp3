"use client";
import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { MainNav } from "./components/main-nav";
import { Graph } from "./components/graph";
import { RecentResults } from "./components/recent-results";
import { UserNav } from "./components/user-nav";

export default function DashboardPage() {
  const [students, setStudents] = useState([]);

  const fetchStudents = async () => {
    const response = await fetch(`/api/student`);
    const data = await response.json();
    setStudents(data);
  };

  const countTypes = (students) => {
    let count = 0;
    if (students)
      students.map((student) => {
        if (student.type) {
          count++;
        }
      });
    return count;
  };

  useEffect(() => {
    fetchStudents();
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
            <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
            <div className="flex items-center space-x-2">
              <Button>Download</Button>
            </div>
          </div>
          <Tabs defaultValue="overview" className="space-y-4">
            <TabsList>
              <TabsTrigger value="overview">Overzicht</TabsTrigger>

              <TabsTrigger value="notifications">Teams</TabsTrigger>
              <TabsTrigger value="analytics">Grafiek</TabsTrigger>
            </TabsList>
            <TabsContent value="overview" className="space-y-4">
              <div className="grid gap-4 m-auto md:grid-cols-2">
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
                    <CardTitle className="text-sm font-medium">
                      Totaal Studenten
                    </CardTitle>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      className="w-4 h-4 text-muted-foreground"
                    >
                      <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
                      <circle cx="9" cy="7" r="4" />
                      <path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" />
                    </svg>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{students.length}</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
                    <CardTitle className="text-sm font-medium">
                      Ingevuld
                    </CardTitle>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      className="w-4 h-4 text-muted-foreground"
                    >
                      <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
                      <circle cx="9" cy="7" r="4" />
                      <path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" />
                    </svg>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">
                      {countTypes(students)}
                    </div>
                    <p className="text-xs text-muted-foreground">
                      {Math.round(
                        (countTypes(students) / students.length) * 100
                      )}
                      % van het totaal
                    </p>
                  </CardContent>
                </Card>
              </div>
              <div className="grid gap-4 md:grid-cols-2">
                <Card className="col-span-3">
                  <CardHeader>
                    <CardTitle>Resultaten</CardTitle>
                    <CardDescription>
                      Er zijn {students.length} resultaten deze week.
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <RecentResults />
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
            <TabsContent value="analytics" className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2 ">
                <Card className="col-span-4">
                  <CardHeader>
                    <CardTitle>Grafiek</CardTitle>
                  </CardHeader>
                  <CardContent className="pl-2">
                    <Graph />
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </>
  );
}
