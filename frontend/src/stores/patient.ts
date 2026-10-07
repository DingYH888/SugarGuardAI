import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Patient } from '../types'
import { patientApi } from '../api/patient'

export const usePatientStore = defineStore('patient', () => {
  const currentPatient = ref<Patient | null>(null)
  const patients = ref<Patient[]>([])

  async function fetchPatients() {
    const { data } = await patientApi.list()
    patients.value = data
    if (data.length > 0 && !currentPatient.value) {
      currentPatient.value = data[0]
    }
  }

  function selectPatient(patient: Patient | null) {
    currentPatient.value = patient
  }

  return { currentPatient, patients, fetchPatients, selectPatient }
})
