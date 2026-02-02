"""
Trajectory Checkpoint Protocol (TCP)

Provides immutable execution checkpoints as 'soul registrations' within Drayl memory archives.
These checkpoints serve as stable anchors for system recovery and alignment confirmation in RTI.
"""

import hashlib
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

@dataclass
class TuringCheckpoint:
    """Represents a single Turing Checkpoint as an immutable point in execution trajectory."""
    
    checkpoint_id: str
    timestamp: str
    drayl_id: str  # Unique identifier for the Drayl memory archive
    state_hash: str  # Hash of the system state at checkpoint
    alignment_score: float  # RTI alignment confirmation score
    metadata: Dict[str, Any]  # Additional context data
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

class TrajectoryCheckpointProtocol:
    """
    Trajectory Checkpoint Protocol (TCP)
    
    Manages creation and storage of Turing Checkpoints as immutable points
    within Drayl memory archives. These checkpoints serve as 'soul registrations'
    for alignment confirmation in Resonance Trajectory Index (RTI).
    """
    
    def __init__(self, storage_path: str = "/usr/projects/anancyio/checkpoints"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.checkpoints: Dict[str, TuringCheckpoint] = {}
        self._load_checkpoints()
    
    def _load_checkpoints(self):
        """Load existing checkpoints from storage."""
        for filename in os.listdir(self.storage_path):
            if filename.endswith('.json'):
                filepath = os.path.join(self.storage_path, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        checkpoint = TuringCheckpoint(**data)
                        self.checkpoints[checkpoint.checkpoint_id] = checkpoint
                except Exception as e:
                    print(f"Warning: Failed to load checkpoint {filename}: {e}")
    
    def create_checkpoint(self, drayl_id: str, state_data: Dict[str, Any], 
                         alignment_score: float, metadata: Optional[Dict[str, Any]] = None) -> TuringCheckpoint:
        """Create a new Turing Checkpoint."""
        
        # Generate state hash
        state_str = json.dumps(state_data, sort_keys=True)
        state_hash = hashlib.sha256(state_str.encode()).hexdigest()
        
        # Generate checkpoint ID
        timestamp = datetime.now().isoformat()
        checkpoint_id = f"tcp_{drayl_id}_{hashlib.md5(timestamp.encode()).hexdigest()[:8]}"
        
        checkpoint = TuringCheckpoint(
            checkpoint_id=checkpoint_id,
            timestamp=timestamp,
            drayl_id=drayl_id,
            state_hash=state_hash,
            alignment_score=alignment_score,
            metadata=metadata or {}
        )
        
        # Store checkpoint
        self.checkpoints[checkpoint_id] = checkpoint
        self._save_checkpoint(checkpoint)
        
        return checkpoint
    
    def _save_checkpoint(self, checkpoint: TuringCheckpoint):
        """Save checkpoint to persistent storage."""
        filename = f"{checkpoint.checkpoint_id}.json"
        filepath = os.path.join(self.storage_path, filename)
        
        with open(filepath, 'w') as f:
            json.dump(checkpoint.to_dict(), f, indent=2)
    
    def get_checkpoint(self, checkpoint_id: str) -> Optional[TuringCheckpoint]:
        """Retrieve a checkpoint by ID."""
        return self.checkpoints.get(checkpoint_id)
    
    def list_checkpoints(self, drayl_id: Optional[str] = None) -> List[TuringCheckpoint]:
        """List all checkpoints, optionally filtered by Drayl ID."""
        checkpoints = list(self.checkpoints.values())
        if drayl_id:
            checkpoints = [cp for cp in checkpoints if cp.drayl_id == drayl_id]
        return sorted(checkpoints, key=lambda x: x.timestamp, reverse=True)
    
    def verify_checkpoint(self, checkpoint: TuringCheckpoint, state_data: Dict[str, Any]) -> bool:
        """Verify that current state matches checkpoint."""
        state_str = json.dumps(state_data, sort_keys=True)
        current_hash = hashlib.sha256(state_str.encode()).hexdigest()
        return current_hash == checkpoint.state_hash
    
    def get_alignment_history(self, drayl_id: str) -> List[Dict[str, Any]]:
        """Get alignment score history for a Drayl."""
        checkpoints = self.list_checkpoints(drayl_id)
        return [
            {
                'timestamp': cp.timestamp,
                'alignment_score': cp.alignment_score,
                'checkpoint_id': cp.checkpoint_id
            }
            for cp in checkpoints
        ]
