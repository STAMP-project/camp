// WARNING: DO NOT EDIT THIS FILE. THIS FILE IS MANAGED BY SPRING ROO.
// You may push code into the target .java compilation unit if you wish to edit any member(s).

package eu.stamp.camp.samples.testman.domain;

import eu.stamp.camp.samples.testman.domain.TCExecStatus;
import eu.stamp.camp.samples.testman.domain.TCExecution;
import java.util.Date;

privileged aspect TCExecution_Roo_JavaBean {
    
    public Date TCExecution.getExecutedOn() {
        return this.executedOn;
    }
    
    public void TCExecution.setExecutedOn(Date executedOn) {
        this.executedOn = executedOn;
    }
    
    public String TCExecution.getTester() {
        return this.tester;
    }
    
    public void TCExecution.setTester(String tester) {
        this.tester = tester;
    }
    
    public TCExecStatus TCExecution.getExecutionStatus() {
        return this.executionStatus;
    }
    
    public void TCExecution.setExecutionStatus(TCExecStatus executionStatus) {
        this.executionStatus = executionStatus;
    }
    
}
