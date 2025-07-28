export interface User {
    id: string;
    name: string;
    age: number;
    email: string;
    createdAt: Date;
}

export interface AssessmentResult {
    userId: string;
    score: number;
    date: Date;
    assessmentType: string;
}

export interface WearableData {
    userId: string;
    heartRate: number;
    steps: number;
    sleepDuration: number;
    date: Date;
}

export interface TelehealthAppointment {
    appointmentId: string;
    userId: string;
    date: Date;
    time: string;
    neuropsychologistId: string;
}

export interface CommunityResource {
    id: string;
    title: string;
    description: string;
    date: Date;
    location: string;
}