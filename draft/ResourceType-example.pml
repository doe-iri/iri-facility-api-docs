/**
 * This is the UML description for the IRI Job class version 1 circa 2025.
 */
@startuml

skinparam class {
    BackgroundColor D0E2F2
    ArrowColor Black
    BorderColor Black
}

skinparam object {
    BackgroundColor D0E2F2
    ArrowColor Black
    BorderColor Black
}

object "Resource:Perlmutter" as perlmutter {
    "name": "Perlmutter",
    "description": "HPE Cray EX supercomputer",
    "resource_type": "system",
    "group": "perlmutter"
}

object "Resource:Scratch" as scratch {
    "name": "Scratch filesystem",
    "description": "NERSC DTNs is mounted at /global/pscratch.",
    "resource_type": "storage",
    "group": "perlmutter"
}

object "Resource:Login" as login {
    "name": "Login",
    "description": "Login Nodes",
    "resource_type": "compute",
    "properties": [
        "cpu_architecture": [ "X86" ],
        "gpu_architecture": [ "NVIDIA_AMPERE" ],
        "drmaa_capability": "ADVANCED_RESERVATION"
    ]
}

object "Resource:Jobs" as jobs {
    "name": "Jobs",
    "description": "Slurm Commands",
    "resource_type": "service"
}

object "Resource:Compute" as compute {
    "name": "Compute",
    "description": "Compute Nodes",
    "resource_type": "compute",
    "properties": [
        "cpu_architecture": [ "X86" ],
        "gpu_architecture": [ "NVIDIA_AMPERE" ],
        "drmaa_capability": "ADVANCED_RESERVATION"
    ]
}

object "Resource::Realtime" as realtime {
    "name": "realtime",
    "description": "Urgent Jobs",
    "resource_type": "compute",
    "group": "perlmutter",
    "properties": [
        "cpu_architecture": [ "X86" ],
        "gpu_architecture": [ "NVIDIA_AMPERE" ],
        "drmaa_capability": "REALTIME_QUEUE",
    ]
}

shifter["shifter (Container Runtimes)"]
scratch["scratch (Scratch)"]

perlmutter --> scratch : "  hasStorage"
perlmutter --> login : "  hasService"
perlmutter --> jobs : "  hasService"
perlmutter --> compute : "  hasCompute"

object "Resource:Spin" as spin {
    "name": "Spin",
    "resource_type": "system"
}

object "Resource:Rancher" as rancher {
    "name": "Rancher",
    "resource_type": "compute"
}

object "Resource:Registry" as registry {
    "name": "Container Registry",
    "resource_type": "service",
    "properties": [
        "architecture": "container",
        "cpu_architecture": "X86",
        "drmaa_capability": "advance_reservation"
    ]
}

spin --> rancher : "  hasService"
spin --> registry : "  hasService"

enum OperatingSystem {
    AIX, 
    BSD, 
    LINUX, 
    HPUX, 
    IRIX, 
    MACOS, 
    SUNOS, 
    TRU64, 
    UNIXWARE, 
    WIN,
    WINNT, 
    OTHER_OS 
}

enum CpuArchitecture {
  ALPHA , ARM , ARM64 , CELL , PARISC , PARISC64 , X86 , X64 , IA64 , MIPS ,
  MIPS64 , PPC , PPC64 , PPC64LE , SPARC , SPARC64 , OTHER_CPU 
}

enum GpuArchitecture {
    NVIDIA_TESLA,
    NVIDIA_FERMI,
    NVIDIA_KEPLER,
    NVIDIA_MAXWELL,
    NVIDIA_PASCAL,
    NVIDIA_VOLTA,
    NVIDIA_TURING,
    NVIDIA_AMPERE,
    NVIDIA_ADA_LOVELACE,
    NVIDIA_HOPPER,
    NVIDIA_BLACKWELL,
    AMD_GCN,
    AMD_RDNA,
    AMD_RDNA2,
    AMD_RDNA3,
    AMD_RDNA4,
    AMD_CDNA,
    INTEL_XE_LP,
    INTEL_XE_HPG,
    INTEL_XE_HPC,
    OTHER_GPU
}

enum DrmaaCapability {
    ADVANCE_RESERVATION,
    REALTIME_QUEUE,
    RESERVE_SLOTS, 
    CALLBACK, 
    BULK_JOBS_MAXPARALLEL,
    JT_EMAIL, 
    JT_STAGING, 
    JT_DEADLINE, 
    JT_MAXSLOTS, 
    JT_ACCOUNTINGID,
    RT_STARTNOW,
    RT_DURATION, 
    RT_MACHINEOS, 
    RT_MACHINEARCH
}

@enduml
