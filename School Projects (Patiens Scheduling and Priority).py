import heapq
import itertools


class Patient:
    def __init__(self, name, surname, id_number, priority):
        self.name = name
        self.surname = surname
        self.id_number = id_number
        self.priority = priority
        self.status = "waiting"

    def print_info(self):
        print(f"{self.name} {self.surname} | ID: {self.id_number} | "
              f"Priority: {self.priority} | Status: {self.status}")


class Scheduler:
    def __init__(self):
        self.patients = []
        self.consultations = []
        self._counter = itertools.count()

    def add_patient(self, patient):
        heapq.heappush(self.patients, (-patient.priority, next(self._counter), patient))
        print(f"Patient {patient.name} {patient.surname} added with priority {patient.priority}.")

    def next_patient(self):
        if self.patients:
            return heapq.heappop(self.patients)[2]
        else:
            print("No patients in the queue.")
            return None

    def print_waiting_list(self):
        if self.patients:
            for _, _, patient in sorted(self.patients):
                patient.print_info()
        else:
            print("No patients in the waiting list.")

    def save_consultations_to_file(self, filename):
        with open(filename, 'w') as file:
            for patient in self.consultations:
                file.write(f"{patient.name},{patient.surname},{patient.id_number},{patient.status}\n")
        print(f"Consultations saved to {filename}.")

    def load_consultations_from_file(self, filename):
        self.consultations.clear()
        try:
            with open(filename, 'r') as file:
                for line in file:
                    name, surname, id_number, status = line.strip().split(',')
                    patient = Patient(name, surname, id_number, 0)
                    patient.status = status
                    self.consultations.append(patient)
            print(f"Consultations loaded from {filename}.")
        except FileNotFoundError:
            print(f"File {filename} not found.")


def main_menu():
    scheduler = Scheduler()
    while True:
        print("\nMain Menu:")
        print("1. Add Patient")
        print("2. Retrieve Next Patient")
        print("3. Print Waiting List")
        print("4. Save Consultations to File")
        print("5. Load Consultations from File")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter patient's name: ")
            surname = input("Enter patient's surname: ")
            id_number = input("Enter patient's ID number: ")

            try:
                priority = int(input("Enter patient's priority (1-5): "))
            except ValueError:
                print("Priority must be a number.")
                continue

            if not 1 <= priority <= 5:
                print("Priority must be between 1 and 5.")
                continue

            patient = Patient(name, surname, id_number, priority)
            scheduler.add_patient(patient)
        elif choice == '2':
            patient = scheduler.next_patient()
            if patient:
                print("Consulting patient:")
                patient.print_info()
                status = input("Enter patient's status after consultation: ")
                patient.status = status
                scheduler.consultations.append(patient)
        elif choice == '3':
            scheduler.print_waiting_list()
        elif choice == '4':
            filename = input("Enter filename to save consultations: ")
            scheduler.save_consultations_to_file(filename)
        elif choice == '5':
            filename = input("Enter filename to load consultations: ")
            scheduler.load_consultations_from_file(filename)
        elif choice == '6':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()