# Copilot Agents Quick Reference

## 🚀 Quick Start

Need help? Choose your agent:

- **HR tasks** → HR Assistant
- **Technical implementation** → Portal Engineer  
- **Code quality/security** → Code Quality Monitor

## 📋 Common Commands

### HR Assistant
```
"Help me implement onboarding checklists"
"Find probation tracking modules on GitHub"
"How do I automate contract renewals?"
"What HR features should I prioritize?"
```

### Portal Engineer
```
"Create an API endpoint for [feature]"
"Implement a React component for [feature]"
"Help me write a database migration"
"Optimize this query performance"
```

### Code Quality Monitor
```
"Scan for security vulnerabilities"
"Check code quality issues"
"Find missing database indexes"
"Identify performance bottlenecks"
```

## 🎯 Decision Tree

```
┌─ Need HR workflow advice?
│  └─→ HR Assistant
│
├─ Want to implement a feature?
│  ├─ Need requirements? → HR Assistant
│  ├─ Need code? → Portal Engineer
│  └─ Need review? → Code Quality Monitor
│
├─ Found a bug?
│  └─→ Portal Engineer
│
├─ Concerned about security?
│  └─→ Code Quality Monitor
│
└─ Want to optimize performance?
   └─→ Code Quality Monitor → Portal Engineer
```

## 📚 Agent Files

- **HR Assistant**: `.github/agents/hr-assistant.md`
- **Portal Engineer**: `.github/agents/portal-engineer.md`
- **Code Quality Monitor**: `.github/agents/code-quality-monitor.md`
- **Full Guide**: `docs/COPILOT_AGENTS.md`
- **Configuration**: `.github/agents/config.yml`

## 🔄 Workflow Templates

### Implementing a New Feature

1. **Plan** (HR Assistant)
   - Define requirements
   - Identify automation opportunities
   
2. **Build** (Portal Engineer)
   - Create database models
   - Implement API endpoints
   - Build frontend components
   
3. **Verify** (Code Quality Monitor)
   - Security scan
   - Code quality check
   - Performance test

### Fixing a Bug

1. **Diagnose** (Code Quality Monitor)
   - Identify root cause
   - Check for related issues
   
2. **Fix** (Portal Engineer)
   - Implement solution
   - Add tests
   
3. **Validate** (Code Quality Monitor)
   - Verify fix works
   - Check for regressions

### Optimizing Performance

1. **Identify** (Code Quality Monitor)
   - Find slow queries
   - Detect N+1 problems
   - Check missing indexes
   
2. **Optimize** (Portal Engineer)
   - Add indexes
   - Optimize queries
   - Implement caching
   
3. **Measure** (Code Quality Monitor)
   - Verify improvements
   - Monitor impact

## 🛠️ Code Patterns

### Backend Pattern
```python
# Router → Service → Repository → Model

# 1. Define model (models/example.py)
class Example(Base):
    __tablename__ = "examples"
    id = Column(Integer, primary_key=True)

# 2. Create schema (schemas/example.py)
class ExampleCreate(BaseModel):
    name: str

# 3. Build repository (repositories/example.py)
class ExampleRepository:
    async def create(self, data): ...

# 4. Add service (services/example.py)
class ExampleService:
    async def create(self, data): ...

# 5. Create router (routers/example.py)
@router.post("/examples")
async def create_example(data: ExampleCreate): ...
```

### Frontend Pattern
```typescript
// Types → Service → Component

// 1. Define types (types/example.ts)
export interface Example {
    id: number;
    name: string;
}

// 2. Create service (services/exampleService.ts)
class ExampleService {
    async list(): Promise<Example[]> { ... }
}

// 3. Build component (components/Example.tsx)
export const ExampleList: React.FC = () => {
    const [items, setItems] = useState<Example[]>([]);
    // ...
}
```

## 🔍 Agent Capabilities Matrix

| Capability | HR Assistant | Portal Engineer | Code Monitor |
|-----------|-------------|----------------|--------------|
| HR Workflows | ✅ Primary | ⚡ Support | ❌ No |
| Feature Planning | ✅ Primary | ⚡ Support | ❌ No |
| Code Implementation | ⚡ Support | ✅ Primary | ❌ No |
| Architecture Design | ⚡ Support | ✅ Primary | ❌ No |
| Security Scanning | ⚡ Support | ⚡ Support | ✅ Primary |
| Code Quality | ❌ No | ⚡ Support | ✅ Primary |
| Performance Optimization | ❌ No | ✅ Primary | ✅ Primary |
| Bug Fixing | ❌ No | ✅ Primary | ⚡ Support |
| Module Discovery | ✅ Primary | ⚡ Support | ❌ No |
| Documentation | ✅ Primary | ⚡ Support | ❌ No |

## 🎓 Learning Resources

### For HR Users
- [HR User Guide](../HR_USER_GUIDE.md) - Portal usage
- [Implementation Plan](../HR_IMPLEMENTATION_PLAN.md) - Feature roadmap
- HR Assistant agent - Ask any questions

### For Developers
- [System Health Check](../SYSTEM_HEALTH_CHECK.md) - Technical overview
- [Recommended Add-ons](../RECOMMENDED_ADDONS.md) - Integrations
- Portal Engineer agent - Technical guidance
- Code Quality Monitor - Best practices

## 🚨 Emergency Procedures

### Critical Security Issue
1. **Alert**: Code Quality Monitor detects critical issue
2. **Assess**: Portal Engineer evaluates impact
3. **Fix**: Portal Engineer implements fix
4. **Verify**: Code Quality Monitor validates
5. **Deploy**: Emergency deployment if needed

### Production Bug
1. **Report**: User reports issue
2. **Diagnose**: Code Quality Monitor identifies cause
3. **Fix**: Portal Engineer resolves
4. **Test**: Verify in staging
5. **Deploy**: Push to production
6. **Monitor**: Code Quality Monitor watches

### Performance Degradation
1. **Detect**: Code Quality Monitor alerts
2. **Analyze**: Identify bottleneck
3. **Optimize**: Portal Engineer fixes
4. **Validate**: Measure improvement
5. **Document**: Update runbooks

## 💡 Tips & Best Practices

### When Asking Questions
- ✅ Be specific with context
- ✅ Include error messages
- ✅ Mention what you've tried
- ✅ Ask for examples
- ❌ Don't ask vague questions
- ❌ Don't skip context

### When Implementing Features
- ✅ Start small
- ✅ Follow existing patterns
- ✅ Test as you go
- ✅ Update documentation
- ❌ Don't skip security checks
- ❌ Don't ignore agent warnings

### When Reviewing Code
- ✅ Use Code Quality Monitor
- ✅ Check security implications
- ✅ Verify performance
- ✅ Test edge cases
- ❌ Don't skip agent scans
- ❌ Don't merge with warnings

## 🎯 Success Metrics

Good agent usage shows:
- ⏱️ Faster feature implementation
- 🐛 Fewer bugs in production
- 🔒 Better security posture
- 📈 Improved code quality
- 📚 Better documentation
- 💡 Team knowledge growth

## 📞 Getting Help

1. **Check this guide** first
2. **Open relevant agent file** for detailed help
3. **Ask specific questions** with context
4. **Follow agent guidance** step-by-step
5. **Provide feedback** to improve agents

## 🔗 Quick Links

- [Full Agent Documentation](../COPILOT_AGENTS.md)
- [HR Assistant Agent](.github/agents/hr-assistant.md)
- [Portal Engineer Agent](.github/agents/portal-engineer.md)
- [Code Quality Monitor](.github/agents/code-quality-monitor.md)
- [Agent Configuration](.github/agents/config.yml)

---

**Remember**: Agents are here to help you build faster, better, and more securely. Don't hesitate to ask questions!
