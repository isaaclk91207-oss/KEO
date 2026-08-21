import os
import uuid
from dotenv import load_dotenv
from agents.orchestrator import create_orchestrator
from agents.registry import create_registry
from config.model_armor import create_model_armor
from config.agent_gateway import create_gateway
from config.audit_logger import create_audit_logger

load_dotenv()

def run_workflow(user_input):
    """Run complete workflow with security"""
    workflow_id = str(uuid.uuid4())[:8]
    
    print(f"\n{'='*60}")
    print(f"WORKFLOW START - ID: {workflow_id}")
    print(f"{'='*60}")
    print(f"Input: {user_input}")
    print(f"{'='*60}\n")
    
    # Initialize security components (local mode - no Firestore needed)
    model_armor = create_model_armor()
    gateway = create_gateway(use_firestore=False)
    audit = create_audit_logger(use_firestore=False)
    orchestrator = create_orchestrator()
    registry = create_registry()
    
    # Step 1: Scan input for PII
    print("[1/5] Scanning input for PII...")
    pii_result = model_armor.protect(user_input, use_gemini=False)
    
    if not pii_result["allowed"]:
        print(f"  BLOCKED: {pii_result['reason']}")
        audit.log_pii_scan(user_input, pii_result["details"], "blocked")
        audit.log_workflow(workflow_id, user_input, [], "blocked_pii")
        return {"status": "blocked", "reason": pii_result["reason"]}
    
    print(f"  SAFE: No PII detected")
    audit.log_pii_scan(user_input, [], "allowed")
    
    # Step 2: Parse intent
    print("\n[2/5] Parsing intent...")
    tasks = orchestrator.parse_intent(pii_result.get("text", user_input))
    print(f"  Found {len(tasks)} tasks:")
    for t in tasks:
        print(f"    - {t.department.value}: {t.action}")
    
    # Step 3: Route tasks with gateway auth
    print("\n[3/5] Routing tasks with authentication...")
    results = []
    
    for task in tasks:
        agent = registry.get_agent(task.department.value)
        if agent:
            # Sign request
            signature = gateway.sign_request("koala_orchestrator", {
                "task": task.action,
                "params": task.params
            })
            
            # Verify before execution
            verified = gateway.verify_request("koala_orchestrator", {
                "task": task.action,
                "params": task.params
            }, signature)
            
            if verified:
                task.status = "running"
                result = agent.execute(task.action, task.params)
                task.result = result
                task.status = "complete"
                results.append(task)
                
                # Log communication
                gateway.log_communication("koala_orchestrator", f"{task.department.value}_agent", task.action, "success")
                
                # Log action
                audit.log_action(f"{task.department.value}_agent", task.action, str(task.params), result)
                
                print(f"    {task.department.value.upper()}: Verified & Executed")
            else:
                print(f"    {task.department.value.upper()}: AUTH FAILED")
                gateway.log_communication("koala_orchestrator", f"{task.department.value}_agent", task.action, "auth_failed")
    
    # Step 4: Display results
    print("\n[4/5] Results:")
    print("-" * 60)
    for task in results:
        print(f"\n  {task.department.value.upper()} Agent:")
        print(f"    Action: {task.action}")
        print(f"    Status: {task.status}")
        if task.result:
            for key, value in task.result.items():
                if key == "posting":
                    print(f"    posting: [Generated - {len(value)} chars]")
                else:
                    print(f"    {key}: {value}")
    
    # Step 5: Log workflow completion
    print("\n[5/5] Logging workflow...")
    tasks_summary = [{"dept": t.department.value, "action": t.action, "status": t.status} for t in results]
    audit.log_workflow(workflow_id, user_input, tasks_summary, "complete")
    
    # Show audit stats
    print("\nAudit Stats:")
    stats = audit.get_stats()
    print(f"  Total actions logged: {stats['total_actions']}")
    print(f"  By agent: {stats['by_agent']}")
    
    print(f"\n{'='*60}")
    print(f"WORKFLOW COMPLETE - ID: {workflow_id}")
    print(f"{'='*60}\n")
    
    return {"status": "complete", "workflow_id": workflow_id, "results": results}

def test_pii_detection():
    """Test PII detection"""
    print("\n" + "="*60)
    print("PII DETECTION TEST")
    print("="*60)
    
    model_armor = create_model_armor()
    
    test_cases = [
        ("Hire a developer with SSN 123-45-6789", "Should block"),
        ("Contact john@company.com for details", "Should redact"),
        ("Budget is $150,000 for this position", "Should redact"),
        ("Normal request without PII", "Should allow")
    ]
    
    for text, expected in test_cases:
        result = model_armor.protect(text)
        status = "BLOCKED" if not result["allowed"] else "SAFE"
        print(f"\n  Input: {text}")
        print(f"  Expected: {expected}")
        print(f"  Result: {status}")
        if result.get("details", {}).get("detected"):
            print(f"  PII Found: {[p['type'] for p in result['details']['detected']]}")

def main():
    print("Koala Fleet - Cross-Department AI Agent")
    print("=" * 60)
    print("Phase 3: Security Layer Active (Local Storage Mode)")
    print("=" * 60)
    
    # Test PII detection
    test_pii_detection()
    
    # Run main workflow
    print("\n" + "="*60)
    print("MAIN WORKFLOW")
    print("="*60)
    user_input = "Hire a Senior Developer, budget $150K, need MacBook Pro"
    results = run_workflow(user_input)
    
    return results

if __name__ == "__main__":
    main()
