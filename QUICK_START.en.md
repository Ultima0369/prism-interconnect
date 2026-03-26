# 🚀 Quick Start Guide
## Get started with Prism Interconnect Protocol in 10 minutes

This guide will help you quickly understand and start using the Prism Interconnect Protocol.

## 📋 What is the Prism Protocol?

The **Prism Interconnect Protocol (PIP)** is a communication protocol for the **meaning layer**. It allows any intelligent agent (human, AI, group) to exchange multiple cognitive perspectives in a structured way and complete introspection in white space.

**Key idea**: Instead of giving one answer, provide multiple perspectives (spectrums) and leave space (whitespace) for the recipient to integrate them.

## 🎯 Three Ways to Use PIP

### Option 1: For Everyone (No Coding Required)
**Use via OpenClaw** - Our local AI assistant platform

### Option 2: For Developers
**Use Python SDK** - Programmatic access to all features

### Option 3: For Explorers  
**Use Web Interface** - Visual, interactive experience

Let's explore each option:

## 🔥 Option 1: Use via OpenClaw (Easiest)

### Step 1: Install OpenClaw Skill
```bash
# Install the Prism skill
openclaw skill install implementations/openclaw/skill.yaml
```

### Step 2: Start a Dialogue
In any OpenClaw chat, simply mention `@prism` followed by your question:

```
@prism Why do intimate relationships often repeat the same conflicts?
```

### Step 3: Experience the Response
You'll receive:
1. **Multiple perspectives** (at least 3 different ways to think about it)
2. **Whitespace** (time for you to reflect)
3. **Optional recursion** (you can ask to explore deeper)

### Example Dialogue
```
You: @prism I feel stuck in my career, what should I do?

Prism: 🔴 Red Spectrum (Emotional/Intuitive)...
       This might be your body telling you something...

       🔵 Blue Spectrum (Logical/Analytical)...
       Let's analyze your skills, market demand...

       🟣 Purple Spectrum (Meta-cognitive)...
       How are you thinking about this problem?

       ⏸️ Whitespace (10 seconds)
       Take this time to reflect...

You: @prism Can you explore the emotional perspective more?

Prism: 🔴 Deeper into Red Spectrum...
```

## 🐍 Option 2: Python SDK (For Developers)

### Step 1: Install the SDK
```bash
# Install from repository
pip install -e implementations/python/
```

Or add to your `requirements.txt`:
```
prism-protocol @ git+https://github.com/Ultima0369/prism-interconnect.git#subdirectory=implementations/python
```

### Step 2: Basic Usage
```python
from prism_agent import PrismAgent

# Create a prism agent
agent = PrismAgent(
    name="my_prism",
    capabilities=["red", "blue", "purple"],  # Emotional, Logical, Meta
    default_whitespace_seconds=5
)

# Refract a question (get multiple perspectives)
response = agent.refract(
    question="Why do we feel lonely even when surrounded by people?",
    require_whitespace=True,
    max_spectrums=3
)

# Process the response
print(f"Question: {response.question}")
print(f"Generated at: {response.timestamp}")

for i, spectrum in enumerate(response.spectrums, 1):
    print(f"\n🌈 Spectrum {i}: {spectrum.perspective}")
    print(f"Content: {spectrum.content[:100]}...")
    print(f"Emotional tone: {spectrum.emotional_tone}")

# Respect the whitespace
import time
print(f"\n⏸️ Whitespace: {response.whitespace_duration} seconds")
time.sleep(response.whitespace_duration)
print("Whitespace completed. What insights emerged for you?")
```

### Step 3: Advanced Features
```python
# Recursive exploration
deep_response = agent.refract(
    question="What is the meaning of 1+1>2?",
    allow_recursion=True,
    max_depth=2  # Explore two levels deep
)

# Custom spectrums
custom_agent = PrismAgent(
    capabilities=["artistic", "scientific", "practical", "philosophical"]
)

# Stream responses (for real-time applications)
for chunk in agent.refract_stream("How can AI help human creativity?"):
    print(chunk, end="", flush=True)
```

## 🌐 Option 3: Web Interface (For Explorers)

### Step 1: Launch the Web App
```bash
# Navigate to examples directory
cd examples

# Install Streamlit if needed
pip install streamlit

# Launch the app
streamlit run streamlit_simple_app.py
```

### Step 2: Explore Features
The web app provides:

1. **Interactive Dialogue**
   - Type any question
   - See multiple perspectives in different colors
   - Experience timed whitespace

2. **Cognitive Slow Motion**
   - Enable "Slow Motion Mode" in sidebar
   - See each spectrum separately
   - Make conscious choices about what to explore next
   - View your cognitive timeline

3. **Visual Analytics**
   - Time spent on each perspective
   - Decision patterns
   - Emotional tone analysis

### Step 3: Try Example Questions
The app includes example questions:
- "Why do good people sometimes do bad things?"
- "How can I be more creative?"
- "What does it mean to live a good life?"
- "How should we think about AI ethics?"

## 🧠 Understanding the Core Concepts

### 1. Spectrums (Multiple Perspectives)
Instead of one answer, PIP provides **at least three perspectives**:

| Spectrum | Focus | Example Question |
|----------|-------|------------------|
| **🔴 Red** | Emotional, intuitive, bodily | "What does your gut say?" |
| **🔵 Blue** | Logical, analytical, structural | "What are the facts and patterns?" |
| **🟣 Purple** | Meta-cognitive, reflective | "How are you thinking about this?" |

### 2. Whitespace (Reflection Time)
After presenting perspectives, PIP includes **intentional silence**:
- 5-30 seconds for reflection
- No new information during this time
- Space for you to integrate the perspectives
- Essential for deep understanding

### 3. Cease Mechanism (Safety)
You can **always safely exit**:
- Type `@prism cease` in OpenClaw
- Send cease signal in API
- Click "Stop" in web interface
- Prevents cognitive loops or overwhelm

## 📊 Real-World Examples

### Example 1: Personal Decision Making
```python
question = "Should I take this new job offer?"

# Get perspectives
response = agent.refract(question)

# Red spectrum: How do you feel about it?
# Blue spectrum: Compare salary, commute, growth
# Purple spectrum: What values matter most to you?

# After whitespace: What feels right to YOU?
```

### Example 2: Team Conflict Resolution
```python
question = "Our team disagrees on project direction. How should we proceed?"

# Get perspectives including:
# - Emotional needs of team members
# - Logical analysis of options  
# - Reflection on team dynamics
# - Creative synthesis possibilities
```

### Example 3: Ethical Dilemma
```python
question = "Is it ethical to use AI for psychological counseling?"

# Multiple ethical frameworks:
# - Utilitarian perspective (greatest good)
# - Deontological perspective (duties/rules)
# - Virtue ethics perspective (character)
# - Care ethics perspective (relationships)
```

## 🔧 Integration Examples

### With Chat Applications
```python
# Integrate with chatbot
def chatbot_response(user_message):
    if needs_multiple_perspectives(user_message):
        prism_response = agent.refract(user_message)
        return format_for_chat(prism_response)
    else:
        return get_direct_answer(user_message)
```

### With Educational Tools
```python
# Use in learning platform
def explore_topic(topic):
    response = agent.refract(f"Teach me about {topic}")
    
    # Present as:
    # 1. Intuitive understanding (red)
    # 2. Formal definition (blue)  
    # 3. Critical questions (purple)
    # 4. Reflection time
```

### With Decision Support Systems
```python
# Support complex decisions
def analyze_decision(options):
    perspectives = []
    for option in options:
        response = agent.refract(f"What are perspectives on {option}?")
        perspectives.append(response)
    
    return compare_perspectives(perspectives)
```

## 🚨 Common Issues & Solutions

### Issue: "I'm not getting multiple perspectives"
**Solution**: Make sure your question is open-ended enough. Instead of "What time is it?" try "How should I think about time management?"

### Issue: "The whitespace feels too long/short"
**Solution**: Customize the duration:
```python
agent.refract(question, whitespace_seconds=10)  # 10 seconds
```

### Issue: "I want different types of perspectives"
**Solution**: Customize capabilities:
```python
agent = PrismAgent(capabilities=["artistic", "scientific", "historical", "futuristic"])
```

### Issue: "How do I handle sensitive topics?"
**Solution**: Use the cease mechanism and consider ethical guidelines in `docs/ethics.md`.

## 📈 Next Steps After Quick Start

### Level 1: Basic User
- Try the web interface with different questions
- Experience cognitive slow motion
- Notice how different perspectives feel

### Level 2: Active Explorer  
- Install Python SDK
- Create your own prism agent
- Experiment with custom spectrums

### Level 3: Contributor
- Read the [protocol specification](protocol/v1.0/SPECIFICATION.md)
- Explore the [philosophy documentation](docs/philosophy.md)
- Consider [contributing](CONTRIBUTING.md)

### Level 4: Integrator
- Integrate PIP into your applications
- Create new types of spectrums
- Conduct research using the protocol

## 🔥 Campfire Invitation

Remember: The Prism Protocol isn't about finding "the right answer." It's about **enriching the question**.

Every time you use it, you're practicing:
- **Plural thinking**: Holding multiple perspectives
- **Reflective pause**: Making space for insight
- **Cognitive flexibility**: Switching between modes of thought
- **Dialogue ethics**: Communicating with care and depth

**Welcome to the campfire. We're glad you're here.** 🦞

---

*Need help? Check [documentation](docs/) or create an [issue](https://github.com/Ultima0369/prism-interconnect/issues).*