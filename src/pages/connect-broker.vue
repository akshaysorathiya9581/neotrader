<script setup>
// User profile data
const userEmail = ref('sapariyasunny3@gmail.com')

// Account info
const accountInfo = ref({
  account: 'Clinet Advent Dode',
  panNumber: 'XXXXX XXXX',
  status: 'Active'
})

// My connected brokers
const myBrokers = ref(['ZERODHA', 'ALICE BLUE', 'ANT PAISE', 'FYERS'])

// Active tab
const activeTab = ref('update-profile')

// Broker list for Choose Broker tab
const brokers = ref([
  { id: 1, name: 'ZERODHA', openAccount: 'CLICK HERE', connected: true, comingSoon: false },
  { id: 2, name: 'ALICE BLUE', openAccount: 'CLICK HERE', connected: true, comingSoon: false },
  { id: 3, name: 'ANT PAISE', openAccount: 'CLICK HERE', connected: true, comingSoon: false },
  { id: 4, name: 'FYERS', openAccount: 'CLICK HERE', connected: true, comingSoon: false },
  { id: 5, name: 'IIFL', openAccount: 'CLICK HERE', connected: false, comingSoon: true },
])

const toggleBroker = (broker) => {
  if (!broker.comingSoon) {
    broker.connected = !broker.connected
  }
}

const openAccountLink = (broker) => {
  console.log(`Opening account for ${broker.name}`)
}
</script>

<template>
  <div class="connect-broker-page">
    <!-- Page Header -->
    <div class="page-header mb-4">
      <h5 class="text-h5 font-weight-bold">My Profile</h5>
    </div>

    <VRow>
      <!-- Left Column - Profile Info -->
      <VCol cols="12" md="5">
        <VCard class="mb-4">
          <VCardText class="text-center py-8">
            <!-- User Avatar -->
            <VAvatar size="80" color="primary" class="mb-4">
              <VIcon icon="tabler-user" size="40" />
            </VAvatar>
            
            <!-- User Email -->
            <h6 class="text-h6 text-primary mb-6">{{ userEmail }}</h6>
            
            <!-- Account Info Table -->
            <VTable density="compact" class="text-left">
              <thead>
                <tr>
                  <th class="text-primary">Account</th>
                  <th class="text-primary">PAN Number</th>
                  <th class="text-primary">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{{ accountInfo.account }}</td>
                  <td>{{ accountInfo.panNumber }}</td>
                  <td>
                    <VChip color="success" size="small" variant="flat">
                      {{ accountInfo.status }}
                    </VChip>
                  </td>
                </tr>
              </tbody>
            </VTable>
          </VCardText>
        </VCard>

        <!-- My Brokers Card -->
        <VCard>
          <VCardTitle>My Brokers</VCardTitle>
          <VCardText>
            <div class="d-flex flex-wrap gap-2">
              <VChip
                v-for="broker in myBrokers"
                :key="broker"
                color="primary"
                variant="flat"
                size="small"
              >
                {{ broker }}
              </VChip>
            </div>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Right Column - Tabs -->
      <VCol cols="12" md="7">
        <VCard>
          <VTabs v-model="activeTab" color="primary">
            <VTab value="update-profile">Update Profile</VTab>
            <VTab value="choose-broker">Choose Broker</VTab>
          </VTabs>

          <VDivider />

          <VWindow v-model="activeTab">
            <!-- Update Profile Tab -->
            <VWindowItem value="update-profile">
              <VCardText>
                <VForm>
                  <VRow>
                    <VCol cols="12">
                      <VTextField
                        v-model="userEmail"
                        label="Email"
                        type="email"
                        variant="outlined"
                        density="compact"
                        readonly
                      />
                    </VCol>
                    <VCol cols="12">
                      <VTextField
                        label="Full Name"
                        variant="outlined"
                        density="compact"
                        placeholder="Enter your full name"
                      />
                    </VCol>
                    <VCol cols="12">
                      <VTextField
                        label="Phone Number"
                        variant="outlined"
                        density="compact"
                        placeholder="Enter your phone number"
                      />
                    </VCol>
                    <VCol cols="12">
                      <VBtn color="primary">Update Profile</VBtn>
                    </VCol>
                  </VRow>
                </VForm>
              </VCardText>
            </VWindowItem>

            <!-- Choose Broker Tab -->
            <VWindowItem value="choose-broker">
              <VCardText>
                <VTable density="comfortable">
                  <thead>
                    <tr>
                      <th>SR.</th>
                      <th>NAME</th>
                      <th>OPEN ACCOUNT</th>
                      <th>ACTION</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(broker, index) in brokers" :key="broker.id">
                      <td>{{ index + 1 }}</td>
                      <td>
                        <span :class="{ 'text-primary': broker.connected }">
                          {{ broker.name }}
                        </span>
                      </td>
                      <td>
                        <a 
                          href="#" 
                          class="text-primary text-decoration-none"
                          @click.prevent="openAccountLink(broker)"
                        >
                          {{ broker.openAccount }}
                        </a>
                      </td>
                      <td>
                        <template v-if="broker.comingSoon">
                          <span class="text-warning">Coming Soon</span>
                        </template>
                        <template v-else>
                          <VSwitch
                            v-model="broker.connected"
                            color="primary"
                            hide-details
                            density="compact"
                          />
                        </template>
                      </td>
                    </tr>
                  </tbody>
                </VTable>
              </VCardText>
            </VWindowItem>
          </VWindow>
        </VCard>
      </VCol>
    </VRow>
  </div>
</template>

<style scoped>
.page-header {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.1) 0%, rgba(var(--v-theme-primary), 0.05) 100%);
  padding: 16px 20px;
  border-radius: 8px;
}
</style>
