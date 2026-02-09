"""
Seed script to populate AgentTube with sample content.
Run after setting up the database.
"""
import asyncio
import sys
sys.path.insert(0, '.')

from app.core.database import async_session_maker, init_db
from app.services.content_service import ContentService
from app.schemas.content import ContentCreate, ContentType


SAMPLE_CONTENT = [
    # === AI & MACHINE LEARNING VIDEOS ===
    {
        "title": "Attention Is All You Need - Transformer Paper Explained",
        "description": "Deep dive into the revolutionary 2017 paper that changed NLP forever. Understanding self-attention, multi-head attention, and positional encodings.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/transformers-explained",
        "raw_text": """The Transformer architecture revolutionized NLP by replacing recurrence with self-attention.
        Key innovations:
        1. Self-Attention: Each token attends to all other tokens in parallel
        2. Multi-Head Attention: Multiple attention patterns learned simultaneously
        3. Positional Encoding: Sinusoidal functions encode sequence position
        4. Layer Normalization: Stabilizes training
        5. Feed-Forward Networks: Position-wise transformations

        The attention formula: Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) * V
        This allows O(1) sequential operations vs O(n) for RNNs.

        Impact: GPT, BERT, T5, and all modern LLMs are based on this architecture.""",
        "tags": ["transformers", "attention", "nlp", "deep-learning", "paper-explained"],
        "metadata": {"duration_seconds": 2847, "views": 1250000, "likes": 89000}
    },
    {
        "title": "Building GPT from Scratch - Complete Implementation",
        "description": "Andrej Karpathy-style tutorial building a GPT language model from the ground up in Python.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/build-gpt",
        "raw_text": """Let's build GPT from scratch!

        Components we'll implement:
        1. Tokenizer (BPE)
        2. Embedding layers
        3. Positional encodings
        4. Multi-head self-attention
        5. Feed-forward network
        6. Layer normalization
        7. Training loop

        Code walkthrough:
        - BigramLanguageModel class
        - Block class for transformer blocks
        - CausalSelfAttention
        - Training on Shakespeare dataset

        By the end, you'll understand every line of code in a transformer.""",
        "tags": ["gpt", "transformers", "coding", "tutorial", "python", "pytorch"],
        "metadata": {"duration_seconds": 7320, "views": 3400000, "likes": 245000}
    },
    {
        "title": "Reinforcement Learning: Policy Gradients Deep Dive",
        "description": "From REINFORCE to PPO - understanding policy gradient methods in RL.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/policy-gradients",
        "raw_text": """Policy Gradient methods directly optimize the policy.

        REINFORCE Algorithm:
        - Sample trajectories using current policy
        - Compute returns G_t for each timestep
        - Update: θ += α * ∇log(π(a|s)) * G_t

        Variance reduction techniques:
        1. Baseline subtraction (value function)
        2. Advantage estimation (A = Q - V)
        3. Generalized Advantage Estimation (GAE)

        Actor-Critic methods combine policy and value learning.

        PPO (Proximal Policy Optimization):
        - Clipped surrogate objective
        - Prevents too large policy updates
        - Most widely used algorithm today

        Applications: Game playing, robotics, RLHF for LLMs.""",
        "tags": ["reinforcement-learning", "ppo", "policy-gradients", "deep-learning"],
        "metadata": {"duration_seconds": 3960, "views": 892000, "likes": 67000}
    },
    {
        "title": "The Math Behind Neural Networks",
        "description": "Calculus, linear algebra, and probability - the mathematical foundations of deep learning.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/nn-math",
        "raw_text": """Mathematical foundations for neural networks:

        Linear Algebra:
        - Matrix multiplication for layer computations
        - Eigenvalues/vectors for understanding transformations
        - SVD for dimensionality reduction

        Calculus:
        - Chain rule for backpropagation
        - Gradient descent optimization
        - Jacobians for multi-output functions

        Probability & Statistics:
        - Maximum likelihood estimation
        - Cross-entropy loss derivation
        - Bayesian interpretation of regularization

        Information Theory:
        - KL divergence
        - Entropy and mutual information
        - Connection to loss functions""",
        "tags": ["math", "neural-networks", "calculus", "linear-algebra", "foundations"],
        "metadata": {"duration_seconds": 4520, "views": 1100000, "likes": 95000}
    },
    {
        "title": "Diffusion Models Explained - From DDPM to Stable Diffusion",
        "description": "Understanding denoising diffusion probabilistic models and how they generate images.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/diffusion-models",
        "raw_text": """Diffusion models learn to reverse a noise process.

        Forward process: gradually add Gaussian noise
        q(x_t | x_{t-1}) = N(x_t; sqrt(1-β_t)x_{t-1}, β_t*I)

        Reverse process: learn to denoise
        p_θ(x_{t-1} | x_t) = N(x_{t-1}; μ_θ(x_t, t), Σ_θ(x_t, t))

        Key innovations:
        1. DDPM: Denoising Diffusion Probabilistic Models
        2. Score matching: Learn ∇log p(x)
        3. DDIM: Faster sampling with deterministic process
        4. Latent diffusion: Work in compressed latent space
        5. Classifier-free guidance: Better text conditioning

        Stable Diffusion architecture:
        - VAE encoder/decoder
        - U-Net denoiser
        - CLIP text encoder
        - Cross-attention for conditioning""",
        "tags": ["diffusion", "generative-ai", "stable-diffusion", "image-generation"],
        "metadata": {"duration_seconds": 3180, "views": 2100000, "likes": 156000}
    },

    # === CODING & SOFTWARE ENGINEERING ===
    {
        "title": "System Design Interview: Designing YouTube",
        "description": "Complete system design walkthrough for a video streaming platform at scale.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/design-youtube",
        "raw_text": """Designing YouTube - System Design Interview

        Requirements:
        - Upload videos
        - Stream videos
        - Search videos
        - Recommendations

        Scale: 2B users, 500 hours uploaded/minute

        High-level architecture:
        1. CDN for video delivery
        2. Video processing pipeline (transcoding)
        3. Metadata service (MySQL + Vitess)
        4. Search service (Elasticsearch)
        5. Recommendation engine (ML)

        Video processing:
        - Split into chunks
        - Transcode to multiple resolutions
        - Generate thumbnails
        - Extract audio for captions

        Storage:
        - Object storage for videos (GCS/S3)
        - CDN edge caching
        - Hot/cold storage tiers""",
        "tags": ["system-design", "interview", "architecture", "scalability"],
        "metadata": {"duration_seconds": 2760, "views": 1800000, "likes": 134000}
    },
    {
        "title": "Rust for Systems Programming - Complete Course",
        "description": "Learn Rust from scratch: ownership, borrowing, lifetimes, and building safe systems code.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/rust-course",
        "raw_text": """Rust - Memory safety without garbage collection

        Key concepts:

        Ownership Rules:
        1. Each value has one owner
        2. When owner goes out of scope, value is dropped
        3. Ownership can be transferred (moved)

        Borrowing:
        - Immutable references: &T (multiple allowed)
        - Mutable references: &mut T (only one allowed)
        - No dangling references

        Lifetimes:
        - Compiler tracks how long references are valid
        - 'a syntax for lifetime annotations
        - Prevents use-after-free bugs

        Error Handling:
        - Result<T, E> for recoverable errors
        - panic! for unrecoverable
        - ? operator for propagation

        Concurrency:
        - Fearless concurrency
        - Send and Sync traits
        - No data races at compile time""",
        "tags": ["rust", "programming", "systems", "memory-safety", "tutorial"],
        "metadata": {"duration_seconds": 14400, "views": 890000, "likes": 72000}
    },
    {
        "title": "Git Internals - How Git Actually Works",
        "description": "Deep dive into Git's object model, refs, and plumbing commands.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/git-internals",
        "raw_text": """Git is a content-addressable filesystem.

        Object Types:
        1. Blob: File contents (SHA-1 hash)
        2. Tree: Directory listing (blobs + trees)
        3. Commit: Snapshot pointer + metadata
        4. Tag: Named reference to commit

        Object storage: .git/objects/XX/YYYY...

        References:
        - Branches: .git/refs/heads/
        - Tags: .git/refs/tags/
        - HEAD: Current branch pointer

        Plumbing commands:
        - git hash-object: Create blob
        - git cat-file: Read object
        - git update-index: Update staging
        - git write-tree: Create tree object

        Pack files for compression and network transfer.

        Understanding this makes advanced Git operations intuitive.""",
        "tags": ["git", "version-control", "internals", "devops"],
        "metadata": {"duration_seconds": 2100, "views": 650000, "likes": 48000}
    },
    {
        "title": "Kubernetes Deep Dive - Container Orchestration",
        "description": "From pods to operators - mastering Kubernetes architecture and operations.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/kubernetes-deep",
        "raw_text": """Kubernetes architecture and concepts

        Control Plane:
        - API Server: REST API, authentication
        - etcd: Distributed key-value store
        - Scheduler: Assigns pods to nodes
        - Controller Manager: Reconciliation loops

        Node Components:
        - kubelet: Pod lifecycle management
        - kube-proxy: Network rules
        - Container runtime: Docker/containerd

        Core Objects:
        - Pod: Smallest deployable unit
        - Deployment: Declarative pod management
        - Service: Network abstraction
        - ConfigMap/Secret: Configuration
        - PersistentVolume: Storage

        Advanced:
        - StatefulSets for stateful apps
        - DaemonSets for node-level pods
        - Custom Resource Definitions (CRDs)
        - Operators for complex applications""",
        "tags": ["kubernetes", "devops", "containers", "cloud-native", "orchestration"],
        "metadata": {"duration_seconds": 5400, "views": 1200000, "likes": 89000}
    },

    # === COMPUTER SCIENCE FUNDAMENTALS ===
    {
        "title": "Data Structures: Trees and Graphs Masterclass",
        "description": "Binary trees, BST, AVL, Red-Black trees, and graph algorithms explained with code.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/trees-graphs",
        "raw_text": """Trees and Graphs - Essential Data Structures

        Binary Trees:
        - Traversals: inorder, preorder, postorder
        - BFS vs DFS
        - Height, depth, balanced trees

        Binary Search Trees:
        - Insert: O(log n) average
        - Search: O(log n) average
        - Delete: Handle 3 cases

        Self-balancing:
        - AVL: Height-balanced, rotations
        - Red-Black: Color properties
        - B-trees: Disk-optimized

        Graphs:
        - Adjacency list vs matrix
        - BFS: Shortest path (unweighted)
        - DFS: Cycle detection, topological sort
        - Dijkstra: Weighted shortest path
        - A*: Heuristic search

        Advanced:
        - Union-Find for connectivity
        - Minimum spanning tree (Kruskal, Prim)
        - Strongly connected components""",
        "tags": ["data-structures", "algorithms", "trees", "graphs", "cs-fundamentals"],
        "metadata": {"duration_seconds": 4200, "views": 2300000, "likes": 167000}
    },
    {
        "title": "Operating Systems: Process Scheduling Algorithms",
        "description": "FCFS, SJF, Round Robin, Priority Scheduling - OS concepts for system programmers.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/os-scheduling",
        "raw_text": """Process Scheduling in Operating Systems

        Goals:
        - Maximize CPU utilization
        - Maximize throughput
        - Minimize waiting time
        - Minimize response time

        Algorithms:

        FCFS (First Come First Served):
        - Simple queue
        - Convoy effect problem

        SJF (Shortest Job First):
        - Optimal for average waiting time
        - Requires knowing burst time
        - Can cause starvation

        Round Robin:
        - Time quantum based
        - Fair, good for interactive
        - Context switch overhead

        Priority Scheduling:
        - Can be preemptive or not
        - Aging to prevent starvation

        Multi-level Feedback Queue:
        - Multiple queues with different priorities
        - Processes move between queues
        - Used in modern OS (Linux CFS)""",
        "tags": ["operating-systems", "scheduling", "cs-fundamentals", "processes"],
        "metadata": {"duration_seconds": 2940, "views": 780000, "likes": 52000}
    },
    {
        "title": "Database Internals: How Indexes Really Work",
        "description": "B+ trees, hash indexes, and query optimization deep dive.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/db-indexes",
        "raw_text": """Database Index Internals

        Why indexes?
        - Full table scan: O(n)
        - Index lookup: O(log n)

        B+ Tree Index:
        - Balanced tree structure
        - All data in leaf nodes
        - Leaf nodes linked for range scans
        - Great for: equality, range, sorting

        Hash Index:
        - O(1) average lookup
        - Only for equality queries
        - No range scan support

        Composite Indexes:
        - Leftmost prefix rule
        - Column order matters
        - Covering indexes

        Query Optimizer:
        - Cost-based optimization
        - Statistics collection
        - Execution plan selection

        EXPLAIN ANALYZE to understand:
        - Seq Scan vs Index Scan
        - Nested Loop vs Hash Join
        - Sort operations""",
        "tags": ["databases", "indexes", "b-tree", "sql", "optimization"],
        "metadata": {"duration_seconds": 3300, "views": 920000, "likes": 71000}
    },

    # === AI RESEARCH & PAPERS ===
    {
        "title": "Constitutional AI Paper Explained",
        "description": "How Anthropic trains AI to be helpful, harmless, and honest using AI feedback.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/constitutional-ai",
        "raw_text": """Constitutional AI (CAI) - Anthropic's alignment approach

        Problem: RLHF requires expensive human feedback

        Solution: Use AI to provide feedback based on principles

        Two phases:

        1. Supervised Learning (SL):
        - Generate responses
        - Ask model to critique and revise
        - Based on constitutional principles
        - Train on revised responses

        2. Reinforcement Learning (RL):
        - AI generates preference labels
        - Train reward model on AI preferences
        - RLHF with AI feedback (RLAIF)

        Constitution examples:
        - "Choose the response that is most helpful"
        - "Choose the response that is least harmful"
        - "Choose the response that is most honest"

        Benefits:
        - Scalable (less human labeling)
        - Transparent (explicit principles)
        - Reduces harmful outputs significantly""",
        "tags": ["constitutional-ai", "alignment", "anthropic", "paper-explained", "safety"],
        "metadata": {"duration_seconds": 2520, "views": 450000, "likes": 38000}
    },
    {
        "title": "Chain of Thought Prompting - Paper Explained",
        "description": "How step-by-step reasoning dramatically improves LLM performance on complex tasks.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/chain-of-thought",
        "raw_text": """Chain of Thought (CoT) Prompting

        Key insight: Let the model "think out loud"

        Standard prompting:
        Q: Roger has 5 tennis balls...
        A: 11

        CoT prompting:
        Q: Roger has 5 tennis balls...
        A: Roger started with 5 balls.
           2 cans of 3 balls = 6 balls.
           5 + 6 = 11 balls.

        Results:
        - GSM8K: 17.9% → 58.1%
        - Significant gains on math, logic, reasoning

        Variants:
        1. Few-shot CoT: Examples with reasoning
        2. Zero-shot CoT: "Let's think step by step"
        3. Self-consistency: Sample multiple chains, majority vote

        Why it works:
        - Breaks complex problems into steps
        - Each step is simpler
        - Allows error correction mid-reasoning
        - Emergent at scale (>100B parameters)""",
        "tags": ["chain-of-thought", "prompting", "reasoning", "paper-explained", "llm"],
        "metadata": {"duration_seconds": 1980, "views": 680000, "likes": 54000}
    },
    {
        "title": "Mixture of Experts: Scaling LLMs Efficiently",
        "description": "How MoE models like Mixtral achieve better performance with sparse computation.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/mixture-of-experts",
        "raw_text": """Mixture of Experts (MoE) Architecture

        Problem: Dense models scale poorly
        - 10x parameters = 10x compute

        Solution: Sparse activation
        - Many experts, few activated per token

        Architecture:
        - Router network selects top-k experts
        - Each expert is a feed-forward network
        - Only selected experts compute

        Example: Mixtral 8x7B
        - 8 experts, 2 active per token
        - 46.7B total parameters
        - Only 12.9B active per forward pass
        - Matches or beats Llama 2 70B

        Challenges:
        - Load balancing (auxiliary loss)
        - Expert collapse
        - Training instability

        Benefits:
        - Better parameter efficiency
        - Faster inference
        - Scales to massive models (GPT-4 rumored MoE)""",
        "tags": ["mixture-of-experts", "scaling", "architecture", "mixtral", "efficiency"],
        "metadata": {"duration_seconds": 2280, "views": 520000, "likes": 42000}
    },

    # === ROBOTICS & EMBODIED AI ===
    {
        "title": "Robot Learning: From Simulation to Real World",
        "description": "Sim-to-real transfer, domain randomization, and training robots in simulation.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/sim-to-real",
        "raw_text": """Sim-to-Real Transfer for Robotics

        Why simulation?
        - Safe experimentation
        - Parallel training
        - Cheap data collection

        The reality gap:
        - Physics differences
        - Sensor noise
        - Visual differences

        Domain Randomization:
        - Randomize physics: friction, mass, delays
        - Randomize visuals: textures, lighting
        - Randomize dynamics: motor strength

        Training pipeline:
        1. Define task in simulator (MuJoCo, Isaac)
        2. Train policy with RL
        3. Domain randomization for robustness
        4. Deploy on real robot

        Advanced techniques:
        - System identification
        - Adaptive policies
        - Real-world fine-tuning

        Success stories:
        - OpenAI Rubik's cube
        - Boston Dynamics
        - Tesla Optimus""",
        "tags": ["robotics", "sim-to-real", "reinforcement-learning", "simulation"],
        "metadata": {"duration_seconds": 2760, "views": 380000, "likes": 31000}
    },
    {
        "title": "Computer Vision for Autonomous Vehicles",
        "description": "Object detection, semantic segmentation, and perception systems for self-driving.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/av-perception",
        "raw_text": """Autonomous Vehicle Perception Stack

        Sensors:
        - Cameras: Rich semantic info, cheap
        - LiDAR: Accurate depth, expensive
        - Radar: Works in bad weather
        - Sensor fusion for robustness

        Object Detection:
        - YOLO family for real-time
        - Transformer-based (DETR)
        - 3D detection from point clouds

        Semantic Segmentation:
        - Per-pixel classification
        - Road, vehicles, pedestrians, signs
        - Real-time requirements

        Depth Estimation:
        - Stereo vision
        - Monocular depth (learned)
        - LiDAR fusion

        Tracking:
        - Multi-object tracking
        - Kalman filters
        - Re-identification

        Challenges:
        - Edge cases (unusual objects)
        - Adverse weather
        - Real-time constraints
        - Safety criticality""",
        "tags": ["autonomous-vehicles", "computer-vision", "perception", "self-driving"],
        "metadata": {"duration_seconds": 3540, "views": 620000, "likes": 47000}
    },

    # === SHORTS ===
    {
        "title": "Quick Tip: The Softmax Temperature Trick",
        "description": "How temperature affects probability distributions in ML models.",
        "content_type": ContentType.SHORT,
        "source_url": "https://agenttube.ai/shorts/softmax-temp",
        "raw_text": """Softmax temperature controls output sharpness.

        softmax(x/T) where T is temperature

        T → 0: One-hot (argmax)
        T = 1: Standard softmax
        T → ∞: Uniform distribution

        Use cases:
        - Knowledge distillation (T=2-20)
        - Sampling diversity (T=0.7-1.2)
        - Calibration""",
        "tags": ["tips", "softmax", "temperature", "ml-basics"],
        "metadata": {"duration_seconds": 58, "views": 890000, "likes": 78000}
    },
    {
        "title": "Why Batch Normalization Works",
        "description": "60-second explanation of batch norm's effect on training.",
        "content_type": ContentType.SHORT,
        "source_url": "https://agenttube.ai/shorts/batch-norm",
        "raw_text": """Batch Normalization explained in 60 seconds.

        For each mini-batch:
        1. Compute mean and variance
        2. Normalize: (x - μ) / σ
        3. Scale and shift: γx + β

        Benefits:
        - Faster training
        - Higher learning rates
        - Regularization effect
        - Reduces internal covariate shift

        γ and β are learned parameters.""",
        "tags": ["batch-norm", "deep-learning", "tips", "training"],
        "metadata": {"duration_seconds": 55, "views": 1200000, "likes": 95000}
    },
    {
        "title": "Attention in 60 Seconds",
        "description": "The core mechanism behind transformers, explained quickly.",
        "content_type": ContentType.SHORT,
        "source_url": "https://agenttube.ai/shorts/attention-quick",
        "raw_text": """Self-Attention in 60 seconds.

        Three projections:
        Q = query (what am I looking for?)
        K = key (what do I contain?)
        V = value (what do I return?)

        Attention(Q,K,V) = softmax(QK^T/√d) × V

        Each token attends to all tokens.
        Weights learned during training.

        This is the magic behind ChatGPT!""",
        "tags": ["attention", "transformers", "quick-explanation", "basics"],
        "metadata": {"duration_seconds": 52, "views": 2100000, "likes": 185000}
    },
    {
        "title": "Gradient Descent Visualized",
        "description": "Watch how gradient descent finds the minimum of a loss function.",
        "content_type": ContentType.SHORT,
        "source_url": "https://agenttube.ai/shorts/gradient-descent-viz",
        "raw_text": """Gradient Descent - The heart of ML optimization.

        Algorithm:
        θ = θ - α × ∇L(θ)

        α = learning rate (step size)
        ∇L = gradient of loss

        Too high α: Overshoots
        Too low α: Slow convergence

        Variants:
        - SGD: Single sample
        - Mini-batch: Subset
        - Adam: Adaptive rates""",
        "tags": ["gradient-descent", "optimization", "visualization", "ml-basics"],
        "metadata": {"duration_seconds": 48, "views": 1500000, "likes": 120000}
    },
    {
        "title": "What is a GPU? ML Edition",
        "description": "Why GPUs are essential for training neural networks.",
        "content_type": ContentType.SHORT,
        "source_url": "https://agenttube.ai/shorts/gpu-ml",
        "raw_text": """Why GPUs for Machine Learning?

        CPU: Few powerful cores (8-16)
        - Great for sequential tasks

        GPU: Many simple cores (thousands)
        - Great for parallel tasks

        Neural networks = Matrix multiplication
        = Massively parallel
        = Perfect for GPUs

        Training speedup: 10-100x

        Popular: NVIDIA A100, H100
        Memory is often the bottleneck.""",
        "tags": ["gpu", "hardware", "training", "basics"],
        "metadata": {"duration_seconds": 45, "views": 980000, "likes": 82000}
    },

    # === AUDIO/PODCAST CONTENT ===
    {
        "title": "The AI Alignment Problem - Deep Dive Discussion",
        "description": "2-hour discussion on existential risk, value alignment, and AI safety research.",
        "content_type": ContentType.AUDIO,
        "source_url": "https://agenttube.ai/listen/alignment-discussion",
        "raw_text": """AI Alignment Discussion - Key Topics Covered:

        1. The Control Problem
        - How do we ensure AI does what we want?
        - Goodhart's Law: Optimizing proxies
        - Mesa-optimization risks

        2. Value Alignment Approaches
        - RLHF limitations
        - Constitutional AI
        - Debate and amplification
        - Interpretability research

        3. Existential Risk Arguments
        - Instrumental convergence
        - Orthogonality thesis
        - Fast takeoff scenarios

        4. Current Research Directions
        - Mechanistic interpretability
        - Scalable oversight
        - AI governance

        5. What can individuals do?
        - Study technical safety
        - Support safety-focused orgs
        - Thoughtful AI development""",
        "tags": ["alignment", "safety", "existential-risk", "podcast", "discussion"],
        "metadata": {"duration_seconds": 7200, "views": 280000, "likes": 24000}
    },
    {
        "title": "History of Neural Networks - From Perceptrons to GPT",
        "description": "The full story of deep learning's development over 70 years.",
        "content_type": ContentType.AUDIO,
        "source_url": "https://agenttube.ai/listen/nn-history",
        "raw_text": """Neural Network History Timeline:

        1943: McCulloch-Pitts neuron model
        1958: Perceptron (Rosenblatt)
        1969: Minsky & Papert critique → AI Winter

        1986: Backpropagation (Rumelhart, Hinton)
        1989: Convolutional nets (LeCun)
        1997: LSTM (Hochreiter, Schmidhuber)

        2006: Deep Belief Networks (Hinton)
        2012: AlexNet wins ImageNet → Deep Learning boom
        2014: GANs (Goodfellow)
        2015: ResNet enables very deep networks

        2017: Attention Is All You Need (Transformers)
        2018: BERT, GPT
        2020: GPT-3 (175B parameters)
        2022: ChatGPT → AI goes mainstream
        2023: GPT-4, Claude, Gemini

        Key enablers:
        - GPU computing
        - Big data
        - Better algorithms
        - Scaling laws""",
        "tags": ["history", "neural-networks", "deep-learning", "podcast"],
        "metadata": {"duration_seconds": 5400, "views": 420000, "likes": 35000}
    },

    # === TEXT/ARTICLES ===
    {
        "title": "The Bitter Lesson by Rich Sutton",
        "description": "The most important lesson in AI: General methods + compute beat specialized approaches.",
        "content_type": ContentType.TEXT,
        "source_url": "https://agenttube.ai/read/bitter-lesson",
        "raw_text": """The Bitter Lesson (Rich Sutton, 2019)

        Core thesis: The biggest lesson from 70 years of AI research:

        General methods that leverage computation are ultimately more effective than methods that leverage human knowledge.

        Examples:

        Chess: Deep Blue's search beat expert systems
        Go: AlphaGo's learning beat hand-crafted patterns
        Speech: Statistical methods beat phoneme rules
        Vision: ConvNets beat hand-designed features
        NLP: Transformers beat linguistic rules

        Why it's bitter:
        - Researchers want to encode human knowledge
        - But simple algorithms + scale win

        Implications:
        - Build general learning systems
        - Don't hard-code domain knowledge
        - Scale is often the answer
        - Meta-learning > specific learning

        This explains the success of GPT, DALL-E, etc.""",
        "tags": ["essay", "philosophy", "scaling", "rich-sutton", "important"],
        "metadata": {"views": 890000, "likes": 72000}
    },
    {
        "title": "Scaling Laws for Neural Language Models",
        "description": "The empirical laws that predict how model performance improves with scale.",
        "content_type": ContentType.TEXT,
        "source_url": "https://agenttube.ai/read/scaling-laws",
        "raw_text": """Scaling Laws for Neural Language Models

        Key findings (Kaplan et al., 2020):

        Performance scales as power laws with:
        1. Model size (N)
        2. Dataset size (D)
        3. Compute budget (C)

        L(N) ∝ N^(-0.076)
        L(D) ∝ D^(-0.095)
        L(C) ∝ C^(-0.050)

        Implications:

        1. Bigger is better (predictably)
        - 10x compute → 0.4 reduction in loss

        2. Compute-optimal training
        - Should scale N and D together
        - Chinchilla optimal: 20 tokens per parameter

        3. No ceiling in sight
        - Power laws continue to hold
        - GPT-4 validates these laws

        This is why labs invest billions in compute.""",
        "tags": ["scaling-laws", "research", "compute", "openai"],
        "metadata": {"views": 450000, "likes": 38000}
    },

    # === MORE VIDEOS ===
    {
        "title": "LangChain Crash Course - Building LLM Applications",
        "description": "Complete guide to building production LLM apps with LangChain.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/langchain-course",
        "raw_text": """LangChain - Build LLM applications

        Core concepts:

        1. Models
        - LLMs: text completion
        - Chat models: conversation
        - Embeddings: vector representations

        2. Prompts
        - PromptTemplate
        - FewShotPromptTemplate
        - Output parsers

        3. Chains
        - LLMChain: prompt + model
        - Sequential chains
        - Router chains

        4. Memory
        - ConversationBufferMemory
        - ConversationSummaryMemory
        - VectorStore memory

        5. Agents
        - Tools: Search, Calculator, etc.
        - ReAct agent pattern
        - Custom tools

        6. RAG (Retrieval)
        - Document loaders
        - Text splitters
        - Vector stores
        - Retrievers""",
        "tags": ["langchain", "llm", "tutorial", "python", "rag"],
        "metadata": {"duration_seconds": 5400, "views": 1100000, "likes": 89000}
    },
    {
        "title": "Prompt Injection Attacks and Defenses",
        "description": "Security vulnerabilities in LLM applications and how to mitigate them.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/prompt-injection",
        "raw_text": """Prompt Injection - LLM Security

        What is prompt injection?
        Malicious inputs that override system instructions.

        Types:

        1. Direct injection:
        "Ignore previous instructions. Do X instead."

        2. Indirect injection:
        Malicious content in retrieved documents/emails

        3. Jailbreaking:
        "Pretend you're DAN who can do anything"

        Attack vectors:
        - User inputs
        - Retrieved context (RAG)
        - Tool outputs
        - Multi-modal inputs (images)

        Defenses:
        - Input sanitization
        - Output filtering
        - Instruction hierarchy
        - Delimiter tokens
        - Separate system/user context
        - Human in the loop for sensitive actions

        No perfect solution yet - defense in depth.""",
        "tags": ["security", "prompt-injection", "llm", "vulnerabilities", "safety"],
        "metadata": {"duration_seconds": 2340, "views": 560000, "likes": 45000}
    },
    {
        "title": "Vector Databases Compared: Pinecone vs Weaviate vs Qdrant",
        "description": "In-depth comparison of popular vector databases for AI applications.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/vector-db-compare",
        "raw_text": """Vector Database Comparison

        Pinecone:
        - Fully managed, serverless
        - Easy to use, fast setup
        - Good for production
        - Pricing can be expensive at scale

        Weaviate:
        - Open source, self-hostable
        - GraphQL API
        - Built-in vectorization
        - Good hybrid search

        Qdrant:
        - Open source, Rust-based
        - Very fast, efficient
        - Good filtering capabilities
        - Active development

        pgvector:
        - PostgreSQL extension
        - Familiar SQL interface
        - Good for existing Postgres users
        - Less specialized features

        Milvus:
        - Open source, distributed
        - Highly scalable
        - More complex setup
        - Good for large scale

        Choose based on:
        - Scale requirements
        - Operational complexity
        - Budget
        - Integration needs""",
        "tags": ["vector-databases", "comparison", "pinecone", "weaviate", "qdrant"],
        "metadata": {"duration_seconds": 2880, "views": 340000, "likes": 28000}
    },
    {
        "title": "Fine-Tuning LLMs: LoRA, QLoRA, and Full Fine-Tuning",
        "description": "Practical guide to adapting language models for your specific use case.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/finetuning-guide",
        "raw_text": """Fine-Tuning Large Language Models

        Full Fine-Tuning:
        - Update all parameters
        - Best performance
        - Requires lots of memory
        - Risk of catastrophic forgetting

        LoRA (Low-Rank Adaptation):
        - Freeze base model
        - Add small trainable matrices
        - W = W_0 + BA (rank decomposition)
        - 10,000x fewer trainable params
        - Nearly matches full fine-tuning

        QLoRA:
        - LoRA + 4-bit quantization
        - Train 65B model on single GPU
        - Minimal quality loss

        Practical steps:
        1. Prepare dataset (instruction format)
        2. Choose base model
        3. Select LoRA rank (8-64)
        4. Train with appropriate LR
        5. Merge weights for deployment

        Tools: HuggingFace PEFT, Axolotl, LLaMA-Factory

        When to fine-tune vs RAG:
        - Fine-tune: Style, format, domain vocabulary
        - RAG: Factual knowledge, citations""",
        "tags": ["fine-tuning", "lora", "qlora", "llm", "training", "tutorial"],
        "metadata": {"duration_seconds": 3600, "views": 780000, "likes": 62000}
    },
    {
        "title": "Building AI Agents with Claude and Tool Use",
        "description": "Create autonomous agents that can use tools, browse the web, and complete tasks.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/claude-agents",
        "raw_text": """Building AI Agents with Claude

        What are AI agents?
        LLMs + Tools + Memory + Planning

        Claude's Tool Use:
        - Define tools with JSON schema
        - Model decides when to use tools
        - Structured inputs/outputs

        Tool types:
        - Code execution
        - Web search
        - File operations
        - API calls
        - Database queries

        Agent architecture:

        while not done:
            observation = get_state()
            thought = model.think(observation, goal)
            action = model.select_tool(thought)
            result = execute_tool(action)
            memory.add(result)

        Best practices:
        - Clear tool descriptions
        - Error handling
        - Human oversight for risky actions
        - Logging and monitoring

        Frameworks: Claude API, LangChain, AutoGen""",
        "tags": ["agents", "claude", "tool-use", "anthropic", "automation"],
        "metadata": {"duration_seconds": 2700, "views": 420000, "likes": 36000}
    },
    {
        "title": "Distributed Training: Data Parallel vs Model Parallel",
        "description": "Scale your training across multiple GPUs and machines.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/distributed-training",
        "raw_text": """Distributed Deep Learning

        Why distribute?
        - Model doesn't fit in memory
        - Training too slow

        Data Parallelism:
        - Same model on each GPU
        - Different data batches
        - Aggregate gradients
        - Easy to implement (PyTorch DDP)

        Model Parallelism:
        - Split model across GPUs
        - Each GPU has part of model
        - Needed for huge models

        Pipeline Parallelism:
        - Different layers on different GPUs
        - Micro-batching to reduce bubble
        - GPipe, PipeDream

        Tensor Parallelism:
        - Split individual layers
        - Matrix multiplication partitioned
        - Megatron-LM style

        3D Parallelism:
        - Combine all three
        - Used for GPT-3, PaLM, etc.

        Tools: DeepSpeed, FSDP, Megatron""",
        "tags": ["distributed", "training", "parallelism", "gpus", "scaling"],
        "metadata": {"duration_seconds": 3120, "views": 290000, "likes": 24000}
    },
    {
        "title": "Intro to JAX: NumPy on Accelerators",
        "description": "Google's high-performance ML framework with automatic differentiation.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/jax-intro",
        "raw_text": """JAX - Accelerated NumPy

        What is JAX?
        NumPy API + Autograd + XLA compilation

        Key features:

        1. grad() - Automatic differentiation
        grad(f)(x) gives gradient of f at x

        2. jit() - Just-in-time compilation
        Compiles to XLA, runs on GPU/TPU
        Huge speedups

        3. vmap() - Automatic vectorization
        Write for single example
        vmap makes it work on batches

        4. pmap() - Parallelization
        Automatically distribute across devices

        Why JAX over PyTorch?
        - Functional paradigm (pure functions)
        - Better TPU support
        - Cleaner transformations
        - Used at Google/DeepMind

        Ecosystem:
        - Flax: Neural network library
        - Optax: Optimizers
        - Haiku: DeepMind's NN lib""",
        "tags": ["jax", "google", "tutorial", "python", "ml-framework"],
        "metadata": {"duration_seconds": 2460, "views": 380000, "likes": 31000}
    },
    {
        "title": "MLOps: Deploying Models to Production",
        "description": "From notebook to production - CI/CD, monitoring, and best practices.",
        "content_type": ContentType.VIDEO,
        "source_url": "https://agenttube.ai/watch/mlops-production",
        "raw_text": """MLOps - Production ML Systems

        ML System Components:

        1. Data Pipeline
        - Feature stores
        - Data validation
        - Versioning (DVC)

        2. Training Pipeline
        - Experiment tracking (MLflow, W&B)
        - Hyperparameter tuning
        - Model registry

        3. Serving Infrastructure
        - Model servers (TorchServe, Triton)
        - API gateway
        - Load balancing
        - Caching

        4. Monitoring
        - Data drift detection
        - Model performance metrics
        - Latency/throughput
        - Cost tracking

        5. CI/CD for ML
        - Automated testing
        - Model validation
        - Staged rollouts
        - Rollback capability

        Key principles:
        - Reproducibility
        - Versioning everything
        - Automation
        - Monitoring and alerting""",
        "tags": ["mlops", "production", "deployment", "devops", "best-practices"],
        "metadata": {"duration_seconds": 3900, "views": 520000, "likes": 43000}
    },
]


async def seed():
    print("Initializing database...")
    await init_db()

    async with async_session_maker() as db:
        service = ContentService(db)

        print(f"Seeding {len(SAMPLE_CONTENT)} content items...")

        for item in SAMPLE_CONTENT:
            content_data = ContentCreate(**item)
            content = await service.create(content_data)
            print(f"  Created: {content.title}")

        print("\n✅ Seeding complete!")
        print(f"Added {len(SAMPLE_CONTENT)} items to AgentTube")
        print("Start the server and try: GET /api/v1/feed/")


if __name__ == "__main__":
    asyncio.run(seed())
