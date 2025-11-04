# Little Monster GPA - Business Process Flows
## Alpha 1.0 - User Journey Diagrams

**Version:** 1.0.0-alpha  
**Date:** November 4, 2025  
**Status:** Current  
**Source:** Consolidated from docs/alpha-0.9/BUSINESS-PROCESS-FLOWS.md

---

## Table of Contents
1. [User Registration & Onboarding](#user-registration--onboarding)
2. [Content Capture Workflows](#content-capture-workflows)
3. [Study Session Workflows](#study-session-workflows)
4. [Social Collaboration Flows](#social-collaboration-flows)
5. [Assessment & Grading Flows](#assessment--grading-flows)

---

## User Registration & Onboarding

### New User Registration Flow

```mermaid
flowchart TD
    Start([User Visits Platform]) --> Landing[Landing Page]
    Landing --> Register{Click Register}
    
    Register --> Form[Registration Form]
    Form --> Input[Enter Details:<br/>- Email<br/>- Password<br/>- Name<br/>- Role]
    
    Input --> Validate{Validate Input}
    Validate -->|Invalid| Error1[Show Error]
    Error1 --> Form
    
    Validate -->|Valid| Submit[Submit to API]
    Submit --> CheckEmail{Email Exists?}
    
    CheckEmail -->|Yes| Error2[Email Taken Error]
    Error2 --> Form
    
    CheckEmail -->|No| Create[Create Account]
    Create --> Hash[Hash Password]
    Hash --> Store[Store in Database]
    Store --> Token[Generate JWT]
    Token --> Session[Create Session]
    Session --> Welcome[Welcome Email]
    
    Welcome --> Redirect[Redirect to Dashboard]
    Redirect --> Onboarding[Show Onboarding]
    Onboarding --> Profile[Complete Profile]
    Profile --> Classes[Join/Create Classes]
    Classes --> Done([Registration Complete])
    
    style Start fill:#90EE90
    style Done fill:#90EE90
    style Error1 fill:#FFB6C1
    style Error2 fill:#FFB6C1
```

---

## Content Capture Workflows

### Photo Capture & OCR Processing

```mermaid
flowchart TD
    Start([Student Opens Camera]) --> Capture[Capture Photo<br/>of Notes/Whiteboard]
    
    Capture --> Upload[Upload Photo]
    Upload --> Validate{Valid Image?}
    
    Validate -->|No| Error[Show Error:<br/>Invalid format]
    Error --> Capture
    
    Validate -->|Yes| Store[Store Original]
    Store --> Queue[Queue OCR Job]
    Queue --> Show[Show Processing Status]
    
    Show --> Process[OCR Worker<br/>Tesseract]
    Process --> Extract[Extract Text]
    Extract --> Analyze[Analyze Content]
    
    Analyze --> Detect{Content Type}
    Detect -->|Handwriting| Hand[Handwriting Recognition]
    Detect -->|Printed Text| Print[Standard OCR]
    Detect -->|Diagram| Diagram[Image Analysis]
    
    Hand --> Combine
    Print --> Combine
    Diagram --> Combine
    
    Combine[Combine Results] --> Vector[Generate Embeddings]
    Vector --> ChromaDB[Store in ChromaDB]
    ChromaDB --> SaveDB[Save Metadata to PostgreSQL]
    
    SaveDB --> Notify[Notify User]
    Notify --> Display[Display in Gallery]
    Display --> Search[Searchable via AI]
    Search --> End([Content Available])
    
    style Start fill:#90EE90
    style End fill:#90EE90
    style Error fill:#FFB6C1
```

### Audio Recording & Transcription Flow

```mermaid
flowchart TD
    Start([User Clicks Record]) --> Perm{Microphone<br/>Permission?}
    
    Perm -->|Denied| PermError[Show Permission<br/>Error]
    PermError --> End1([Cannot Record])
    
    Perm -->|Granted| Init[Initialize Audio Stream]
    Init --> Record[Recording...]
    Record --> Display[Show Waveform<br/>& Timer]
    
    Display --> Stop{Stop Recording}
    Stop --> Save[Save Audio File]
    Save --> Preview[Show Preview<br/>Play/Delete/Upload]
    
    Preview --> Delete{User Action}
    Delete -->|Delete| Discard([Discard Recording])
    Delete -->|Upload| Upload[Upload to Server]
    
    Upload --> ValidSize{File Size OK?}
    ValidSize -->|Too Large| SizeError[File Too Large<br/>Max 50MB]
    SizeError --> Preview
    
    ValidSize -->|OK| StoreAudio[Store Audio File]
    StoreAudio --> QueueJob[Queue Transcription Job]
    QueueJob --> JobID[Return Job ID]
    
    JobID --> ShowStatus[Show Progress Bar]
    ShowStatus --> Worker[STT Worker Processes]
    Worker --> Whisper[Whisper Model<br/>Transcription]
    Whisper --> Store[Store Transcript]
    Store --> Vector[Create Embeddings]
    Vector --> ChromaDB[Store in ChromaDB]
    
    ChromaDB --> Complete[Update Job Status]
    Complete --> Notify[Notify User]
    Notify --> ShowResult[Display Transcript]
    ShowResult --> Options[Options:<br/>- Edit<br/>- Search<br/>- Export<br/>- Share]
    
    Options --> End2([Transcription Complete])
    
    style Start fill:#90EE90
    style End1 fill:#FFB6C1
    style End2 fill:#90EE90
    style PermError fill:#FFB6C1
    style SizeError fill:#FFB6C1
```

---

## Study Session Workflows

### AI Chat Study Session

```mermaid
sequenceDiagram
    actor Student
    participant Web
    participant Gateway
    participant Auth
    participant LLM
    participant RAG
    participant ChromaDB
    participant Bedrock
    participant DB
    
    Student->>Web: Ask Question
    Web->>Gateway: POST /api/chat/completions
    Gateway->>Auth: Validate JWT
    Auth-->>Gateway: Valid
    
    Gateway->>LLM: Forward Question
    
    alt Use RAG
        LLM->>RAG: Search Context
        RAG->>ChromaDB: Similarity Search
        ChromaDB-->>RAG: Relevant Docs
        RAG->>RAG: Build Context
        RAG-->>LLM: Context + Question
    end
    
    LLM->>Bedrock: Generate Response
    Bedrock-->>LLM: AI Response
    
    LLM->>DB: Log Interaction
    LLM-->>Gateway: Response
    Gateway-->>Web: Display Answer
    Web-->>Student: Show Response
    
    Student->>Web: Follow-up Question
    Note over Student,Bedrock: Process continues...
```

### Flashcard Study Flow

```mermaid
stateDiagram-v2
    [*] --> SelectDeck: Choose Deck
    SelectDeck --> Configure: Set Options
    Configure --> ShowFront: Display Front
    
    ShowFront --> Thinking: Student Thinks
    Thinking --> Reveal: Reveal Answer
    
    Reveal --> Rate: Self-Rate
    
    Rate --> Easy: Easy
    Rate --> Good: Good
    Rate --> Hard: Hard
    Rate --> Again: Again
    
    Easy --> NextCard
    Good --> NextCard
    Hard --> NextCard
    Again --> Later: Review Later
    
    Later --> NextCard: Add to Queue
    
    NextCard --> CheckRemaining: Cards Left?
    CheckRemaining --> ShowFront: Yes
    CheckRemaining --> Complete: No
    
    Complete --> Stats: Show Statistics
    Stats --> UpdateProgress: Update Progress
    UpdateProgress --> Points: Award Points
    Points --> [*]
    
    note right of Rate
        Spaced Repetition Algorithm:
        - Easy: 4 days
        - Good: 1 day
        - Hard: 10 minutes
        - Again: Immediately
    end note
```

---

## Social Collaboration Flows

### Group Study Session Flow

```mermaid
flowchart TD
    Start([Student Initiates<br/>Group Study]) --> Create{Create or Join?}
    
    Create -->|Create New| NewGroup[Create Study Group]
    Create -->|Join Existing| FindGroup[Browse Groups]
    
    NewGroup --> SetName[Set Group Name]
    SetName --> SelectClass[Select Class/Topic]
    SelectClass --> Privacy{Privacy Setting}
    
    Privacy -->|Public| Public[Anyone Can Join]
    Privacy -->|Private| Private[Invite Only]
    
    Public --> Invite
    Private --> Invite[Invite Members]
    
    FindGroup --> Browse[View Available Groups]
    Browse --> Select[Select Group]
    Select --> Request{Approval Required?}
    
    Request -->|Yes| WaitApproval[Wait for Approval]
    Request -->|No| JoinDirect[Join Directly]
    WaitApproval --> Approved{Approved?}
    Approved -->|No| End1([Join Denied])
    Approved -->|Yes| JoinDirect
    
    Invite --> InGroup[In Study Group]
    JoinDirect --> InGroup
    
    InGroup --> Activities{Group Activities}
    
    Activities -->|Chat| GroupChat[Real-time Chat]
    Activities -->|Share Notes| ShareNotes[Share Study Materials]
    Activities -->|Collaborate| Collab[Collaborative Documents]
    Activities -->|Q&A| QA[Ask/Answer Questions]
    
    GroupChat --> Notifications
    ShareNotes --> Notifications
    Collab --> Notifications
    QA --> Notifications[Push Notifications<br/>to Members]
    
    Notifications --> Track[Track Participation]
    Track --> Points[Award Points]
    Points --> Leaderboard[Update Group Leaderboard]
    
    Leaderboard --> Continue{Continue?}
    Continue -->|Yes| Activities
    Continue -->|No| Leave[Leave Group]
    Leave --> End2([Session Complete])
    
    style Start fill:#90EE90
    style End1 fill:#FFB6C1
    style End2 fill:#90EE90
```

---

## Assessment & Grading Flows

### Assignment Submission Flow

```mermaid
flowchart TD
    Start([Student Views<br/>Assignment]) --> View[Read Instructions]
    View --> Check{Has Attachments?}
    
    Check -->|No| TextOnly[Text-only Submission]
    Check -->|Yes| Upload[Upload Files]
    
    TextOnly --> Editor[Rich Text Editor]
    Upload --> FileTypes{File Types}
    
    FileTypes -->|PDF| PDF[Process PDF]
    FileTypes -->|Images| Images[Process Images]
    FileTypes -->|Audio| Audio[Process Audio]
    FileTypes -->|Video| Video[Process Video]
    
    PDF --> Validate
    Images --> Validate
    Audio --> Queue[Queue for Processing]
    Video --> Queue
    
    Queue --> Async[Async Processing]
    Async --> Validate{Validate Submission}
    
    Editor --> Validate
    
    Validate -->|Invalid| Error[Show Validation Errors]
    Error --> View
    
    Validate -->|Valid| Confirm[Confirmation Dialog]
    Confirm --> Submit{Submit?}
    
    Submit -->|Cancel| View
    Submit -->|Confirm| Process[Submit to Server]
    
    Process --> Store[Store Submission]
    Store --> Timestamp[Record Timestamp]
    Timestamp --> LateCheck{Past Deadline?}
    
    LateCheck -->|Yes| LatePenalty[Apply Late Penalty]
    LateCheck -->|No| OnTime[Mark On Time]
    
    LatePenalty --> NotifyTeacher
    OnTime --> NotifyTeacher[Notify Teacher]
    
    NotifyTeacher --> NotifyStudent[Confirm to Student]
    NotifyStudent --> Receipt[Show Receipt]
    Receipt --> Track[Track in Progress]
    
    Track --> Wait[Wait for Grading]
    Wait --> Grade{Teacher Grades}
    
    Grade --> Score[Record Score]
    Score --> Feedback[Add Feedback]
    Feedback --> UpdateGPA[Update GPA]
    UpdateGPA --> NotifyGrade[Notify Student]
    NotifyGrade --> ShowGrade[Show Grade & Feedback]
    
    ShowGrade --> End([Assignment Complete])
    
    style Start fill:#90EE90
    style End fill:#90EE90
    style Error fill:#FFB6C1
```

---

## Reference

All diagrams are maintained in Git with version control. For additional system architecture diagrams, see:
- ARCHITECTURE-DIAGRAMS.md (technical architecture diagrams)
- TECHNICAL-ARCHITECTURE.md (system architecture documentation)
