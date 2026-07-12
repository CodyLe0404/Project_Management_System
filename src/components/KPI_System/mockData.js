/**
 * Mock data for the Personal KPI & Project Tracking Dashboard.
 * Ready to be imported in a Vue 3 component.
 */
export const mockMembers = [
  {
    id: 1,
    name: "Alex Nguyen",
    avatar: "/src/assets/image_profile/pic2.jpg",
    role: "Project Manager",
    mainTasksCount: 12,
    subTasksCount: 34,
    onTime: 28,
    aheadOfSchedule: 14,
    delayed: 4,
    projects: [
      { projectName: "Customer Portal Redesign", projectStatus: "Doing" },
      { projectName: "Internal HR System Upgrade", projectStatus: "Ahead of schedule" },
      { projectName: "API Gateway Integration", projectStatus: "On Time" },
      { projectName: "API Gateway Integration", projectStatus: "On Time" },
      { projectName: "API Gateway Integration", projectStatus: "On Time" },
      { projectName: "API Gateway Integration", projectStatus: "On Time" },
      { projectName: "API Gateway Integration", projectStatus: "On Time" },
      { projectName: "API Gateway Integration", projectStatus: "On Time" },
      { projectName: "API Gateway Integration", projectStatus: "On Time" },
      { projectName: "API Gateway Integration", projectStatus: "On Time" },
      { projectName: "AI Recommendations Engine", projectStatus: "Not yet start" }
    ]
  },
  {
    id: 2,
    name: "Sarah Chen",
    avatar: "/src/assets/image_profile/pic5.jpg",
    role: "Frontend Team Lead",
    mainTasksCount: 18,
    subTasksCount: 42,
    onTime: 38,
    aheadOfSchedule: 18,
    delayed: 4,
    projects: [
      { projectName: "Customer Portal Redesign", projectStatus: "Doing" },
      { projectName: "E-Commerce Checkout Optimization", projectStatus: "On Time" },
      { projectName: "Design System V2", projectStatus: "Ahead of schedule" }
    ]
  },
  {
    id: 3,
    name: "Marcus Brodie",
    avatar: "/src/assets/image_profile/pic8.avif",
    role: "Senior Backend Developer",
    mainTasksCount: 15,
    subTasksCount: 38,
    onTime: 26,
    aheadOfSchedule: 20,
    delayed: 7,
    projects: [
      { projectName: "API Gateway Integration", projectStatus: "On Time" },
      { projectName: "Billing Service Refactor", projectStatus: "Delay" },
      { projectName: "AI Recommendations Engine", projectStatus: "Not yet start" }
    ]
  },
  {
    id: 4,
    name: "Elena Rostova",
    avatar: "/src/assets/image_profile/pic6.jpg",
    role: "UI/UX Designer",
    mainTasksCount: 10,
    subTasksCount: 28,
    onTime: 20,
    aheadOfSchedule: 15,
    delayed: 3,
    projects: [
      { projectName: "Customer Portal Redesign", projectStatus: "Doing" },
      { projectName: "Design System V2", projectStatus: "Ahead of schedule" },
      { projectName: "Mobile App Wireframes", projectStatus: "No plan" }
    ]
  },
  {
    id: 5,
    name: "David Kim",
    avatar: "/src/assets/image_profile/pic10.jpg",
    role: "QA Automation Engineer",
    mainTasksCount: 8,
    subTasksCount: 52,
    onTime: 40,
    aheadOfSchedule: 10,
    delayed: 10,
    projects: [
      { projectName: "E-Commerce Checkout Optimization", projectStatus: "On Time" },
      { projectName: "Billing Service Refactor", projectStatus: "Delay" },
      { projectName: "End-to-End Regression Suite", projectStatus: "Doing" }
    ]
  },
  {
    id: 6,
    name: "Aaliyah Jackson",
    avatar: "/src/assets/image_profile/pic3.jpg",
    role: "DevOps Engineer",
    mainTasksCount: 14,
    subTasksCount: 31,
    onTime: 32,
    aheadOfSchedule: 8,
    delayed: 5,
    projects: [
      { projectName: "API Gateway Integration", projectStatus: "On Time" },
      { projectName: "AWS Cloud Migration", projectStatus: "Doing" },
      { projectName: "CI/CD Pipeline Security Audit", projectStatus: "No plan" }
    ]
  }
];
