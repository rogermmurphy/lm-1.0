# Business Process Flow Diagrams
## Alpha 0.9 - User Journeys & System Workflows

**Version:** 0.9.0-alpha  
**Date:** November 2, 2025  

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

### Login Flow

```mermaid
sequenceDiagram
    actor User
    participant Web as Web App
    participant Gateway as API Gateway
    participant Auth as Auth Service
    participant DB as PostgreSQL
    participant Redis
    
    User->>Web: Enter credentials
    Web->>Gateway: POST /api/auth/login
    Gateway->>Auth: Forward request
    
    Auth->>DB: Find user by email
    DB-->>Auth: User record
    
    Auth->>Auth: Verify password hash
    
    alt Password Valid
        Auth->>Auth: Generate JWT
        Auth->>DB: Create session
        Auth->>Redis: Cache session
        Auth-->>Gateway: JWT + user data
        Gateway-->>Web: 200 OK + token
        Web->>Web: Store token
        Web->>User: Redirect to dashboard
    else Password Invalid
        Auth-->>Gateway: 401 Unauthorized
        Gateway-->>Web: Login failed
        Web->>User: Show error message
    end
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

### Study Tools Generation Flow

```mermaid
flowchart TD
    Start([Student Selects<br/>Study Material]) --> Choose{Choose Tool}
    
    Choose -->|Generate Notes| Notes[AI Notes Generation]
    Choose -->|Create Flashcards| Flash[Flashcard Generation]
    Choose -->|Practice Test| Test[Test Generation]
    
    Notes --> FetchContent[Fetch Source Content]
    Flash --> FetchContent
    Test --> FetchContent
    
    FetchContent --> RAGSearch[Search Related Materials<br/>via RAG]
    RAGSearch --> Context[Build Context]
    Context --> Prompt[Generate AI Prompt]
    
    Prompt --> LLM{LLM Provider}
    LLM -->|Dev| Ollama[Ollama Local]
    LLM -->|Prod| Bedrock[AWS Bedrock]
    
    Ollama --> Generate
    Bedrock --> Generate[Generate Content]
    
    Generate --> Format[Format Output]
    Format --> Validate{Quality Check}
    
    Validate -->|Poor Quality| Regenerate[Regenerate]
    Regenerate --> Generate
    
    Validate -->|Good| Store[Store Generated Content]
    Store --> Points[Award Points]
    Points --> Notify[Notify Student]
    Notify --> Display[Display Result]
    
    Display --> Actions{Student Action}
    Actions -->|Edit| Edit[Edit Mode]
    Actions -->|Export| Export[Export to PDF/DOCX]
    Actions -->|Share| Share[Share with Class]
    Actions -->|Save| Save[Save to Library]
    
    Edit --> Save
    Export --> Done
    Share --> Done
    Save --> Done([Content Saved])
    
    style Start fill:#90EE90
    style Done fill:#90EE90
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

### Content Sharing Workflow

```mermaid
sequenceDiagram
    actor Student A
    participant Web
    participant Gateway
    participant Social
    participant Notif
    participant DB
    actor Student B
    
    Student A->>Web: Select content to share
    Web->>Web: Choose recipients
    Student A->>Web: Add message & click share
    
    Web->>Gateway: POST /api/social/share
    Gateway->>Social: Process share request
    
    Social->>DB: Check permissions
    Social->>DB: Create share record
    Social->>DB: Log activity
    
    Social->>Notif: Trigger notification
    Notif->>DB: Store notification
    Notif->>Notif: Push to recipients
    
    Social-->>Gateway: Share successful
    Gateway-->>Web: Confirmation
    Web->>Student A: Show success message
    
    Notif-->>Student B: Push Notification
    Student B->>Web: Click notification
    Web->>Gateway: GET /api/social/shares/:id
    Gateway->>Social: Fetch shared content
    Social->>DB: Get content details
    DB-->>Social: Content data
    Social-->>Gateway: Content
    Gateway-->>Web: Display
    Web->>Student B: View shared content
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

### AI-Assisted Grading Flow (Teacher Side)

```mermaid
flowchart TD
    Start([Teacher Views<br/>Submissions]) --> List[List All Submissions]
    List --> Select[Select Submission]
    Select --> View[View Student Work]
    
    View --> AI{Use AI<br/>Assistance?}
    
    AI -->|No| ManualGrade[Manual Grading]
    AI -->|Yes| Analyze[AI Content Analysis]
    
    Analyze --> Rubric[Check Against Rubric]
    Rubric --> Quality[Assess Quality]
    Quality --> Plagiarism[Plagiarism Check]
    Plagiarism --> Suggest[Suggest Grade<br/>& Comments]
    
    Suggest --> Review[Teacher Reviews AI Suggestions]
    
    Review --> Adjust{Adjust Grade?}
    Adjust -->|Yes| Modify[Modify Grade/Comments]
    Adjust -->|No| Accept[Accept AI Suggestion]
    
    ManualGrade --> Assign
    Modify --> Assign[Assign Final Grade]
    Accept --> Assign
    
    Assign --> Record[Record in Database]
    Record --> UpdateGPA[Recalculate Student GPA]
    UpdateGPA --> Notify[Notify Student]
    Notify --> Points[Award Teacher Points]
    
    Points --> Next{More Submissions?}
    Next -->|Yes| List
    Next -->|No| Summary[View Grading Summary]
    Summary --> Stats[Class Statistics]
    Stats --> End([Grading Complete])
    
    style Start fill:#90EE90
    style End fill:#90EE90
```

---

## Study Session Workflows

### Complete Study Session Flow

```mermaid
flowchart TD
    Start([Student Starts<br/>Study Session]) --> Timer[Start Timer]
    Timer --> Topic[Select Topic]
    Topic --> Materials[Gather Materials]
    
    Materials --> Activities{Study Activities}
    
    Activities -->|Read| Read[Read Content]
    Activities -->|Practice| Practice[Practice Problems]
    Activities -->|Watch| Watch[Watch Video]
    Activities -->|Listen| Listen[Audio Lecture]
    Activities -->|Review| Review[Review Notes]
    
    Read --> Track
    Practice --> Track
    Watch --> Track
    Listen --> Transcribe[Auto-Transcribe]
    Review --> Track
    
    Transcribe --> Track[Track Progress]
    
    Track --> Log[Log Activity]
    Log --> Points[Earn Points]
    Points --> Check{Understanding?}
    
    Check -->|Confused| AskAI[Ask AI Tutor]
    AskAI --> Explain[Get Explanation]
    Explain --> Check
    
    Check -->|Clear| Continue{Continue?}
    Continue -->|Yes| Activities
    Continue -->|No| End[End Session]
    
    End --> StopTimer[Stop Timer]
    StopTimer --> Summary[Generate Summary]
    Summary --> Stats[Session Statistics:<br/>- Time spent<br/>- Topics covered<br/>- Points earned<br/>- Progress made]
    
    Stats --> Save[Save Session Data]
    Save --> Analytics[Update Analytics]
    Analytics --> Suggest[AI Suggestions<br/>for Next Session]
    
    Suggest --> Done([Session Complete])
    
    style Start fill:#90EE90
    style Done fill:#90EE90
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

## Real-Time Collaboration Flows

### Live Chat in Study Group

```
Real-Time Chat Flow:

Student A                    Server                    Student B
    │                          │                          │
    │  1. Connect WebSocket    │                          │
    ├─────────────────────────▶│                          │
    │  ← Connected              │  2. Connect             │
    │                          │◀─────────────────────────┤
    │                          │  ← Connected             │
    │                          │                          │
    │  3. Type Message         │                          │
    ├─────────────────────────▶│                          │
    │                          │  4. Broadcast            │
    │                          ├─────────────────────────▶│
    │                          │                          │  5. Display
    │  6. Typing Indicator     │                          │
    ├────────────────────────
